from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from app.db import get_db
from bson import timestamp
import random

api = Blueprint('api', __name__)


# 获取错题列表, 默认不包括不重要的
@api.route('/wqs', methods=['GET'])
@login_required
def get_wrong_questions():
    dismissed = request.args.get('dismissed', default=False, type=bool)
    category = request.args.get('category', default=None, type=str)
    uid = current_user.get_id()
    query = {"uid": uid, "dismissed": dismissed}
    if category:
        query['category'] = category
    print(uid)
    return jsonify(get_all_question_dict(query))


def get_all_question_dict(query):
    questions = get_all_question(query)
    return transfer_question_dict(questions)


def get_all_question(query):
    db = get_db()
    questions = db.question.find(query)
    # gfs = GridFS(db, collection='question')
    # pic_results = gfs.find(query)
    return questions


def transfer_question_dict(questions):
    resp = {
        "questions": [
            {
                '_id': str(q['_id']),
                'description': q['description'] if 'description' in q else '',
                'category': q['category'],
                'dismissed': q['dismissed'],
                'answer': q['answer'],
                'date': q['date'].time * 1000,
                'url': q['url'] if 'url' in q else None
            } for q in questions
        ] 
    }
    return resp


@api.route('/wqs_file', methods=['POST', 'PUT'])
@login_required
def update_wrong_questions_file():
    uid = current_user.get_id()
    db = get_db()
    resp = {}

    f = request.files['file']
    question = {'uid': uid}
    question['description'] = request.form.get('description')
    question['date'] = timestamp.Timestamp(int(request.form.get('date')) // 1000, 1)
    question['fname'] = f.filename
    question['dismissed'] = bool(request.form.get('dismissed')) == True
    question['category'] = request.form.get('category')
    question['answer'] = request.form.get('answer')

    import requests

    def upload_to_smms(f):
        smms_url = 'https://sm.ms/api/upload'
        file = {'smfile': f}
        data_result=requests.post(smms_url,data=None,files=file)
        # print(data_result.json())
        return data_result.json()

    if request.method == 'PUT':
        _id = request.form.get('_id')
        condition = {'uid': uid, '_id': ObjectId(_id)}
        ori_question = db.question.find_one(condition)
        if not ori_question:
            resp['success'] = False
            resp['message'] = '_id not found'
            return jsonify(resp)
        else:
            delete_url = ori_question['delete']
            requests.get(delete_url)  # delete

    # upload picture
    data_result = upload_to_smms(f)
    smms_result = data_result['success']
    # smms_code = data_result['code']
    smms_message = data_result['message']

    resp['success'] = smms_result
    resp['message'] = smms_message

    if smms_result is True:
        data = data_result['data']
        # store data dictionary to MongoDB
        # data_keys = ['width', 'height', 'size', 'path', 'hash', 'url', 'delete', 'page', 'RequestId']  # 'filename','storename','file_id',
        del data['filename'], data['storename'], data['file_id']
        question.update(data)
        if request.method == 'PUT':
            ori_question.update(data)
            ori_question.update(question)
            update_result = db.question.update_one(condition, {'$set': ori_question})
            # print(result.raw_result)
            resp['matched_count'] = update_result.matched_count
            resp['modified_count'] = update_result.modified_count
        elif request.method == 'POST':
            result = db.question.insert_one(question)
            resp['_id'] = str(result.inserted_id)
        return jsonify(resp)
    else:
        # smms_images = data_result['images']
        # smms_request_id = data_result['RequestId']
        return jsonify(resp)


@api.route('/wqs', methods=['POST', 'PUT'])
@login_required
def update_wrong_questions():
    uid = current_user.get_id()
    db = get_db()
    resp = {}
    # upload text question by json
    def load_request_attr(question, request):
        question_attrs = ['description', 'answer', 'dismissed', 'category', 'date']
        for attr_name in question_attrs:
            attr = request.json.get(attr_name)
            if attr_name == 'date':
                attr = timestamp.Timestamp(int(attr) // 1000, 1)
            question[attr_name] = attr

    if request.method == 'POST':
        # 上传错题
        question = {'uid': uid}
        load_request_attr(question, request)
        result = db.question.insert_one(question)
        resp['_id'] = str(result.inserted_id)
        return jsonify(resp)

    elif request.method == 'PUT':
        # 更新错题
        _id = request.json.get('_id')
        obj_id = ObjectId(_id)
        condition = {'uid':uid, '_id':obj_id}
        ori_question = db.question.find_one(condition)
        load_request_attr(ori_question, request)
        result = db.question.update_one(condition, {'$set': ori_question})
        # print(result.raw_result)
        resp['matched_count'] = result.matched_count
        resp['modified_count'] = result.modified_count
        return jsonify(resp)


@api.route('/wqs/<string:wq_id>', methods=['DELETE'])
@login_required
def delete_wrong_question(wq_id: str):
    uid = current_user.get_id()
    db = get_db()
    wq_id = ObjectId(wq_id)
    q = db.question.find_one({'_id': wq_id})
    if not q:
        abort(404)
    db.question.delete_one({'_id': wq_id})
    return jsonify({'status': 'Success'})


@api.route('/wqs/categories', methods=['GET'])
@login_required
def get_categories():
    uid = current_user.get_id()
    db = get_db()
    res = db.question.distinct('category')
    # res = db.question.find({'uid': uid})
    # categories = set([_['category'] for _ in res])
    # resp = {'categories': list(categories)}
    return jsonify(res)


@api.route('/quiz', methods=['GET'])
@login_required
def get_all_quizzes():
    uid = current_user.get_id()
    db = get_db()
    quizzes = db.quiz.find({'uid': uid})
    resp = {'quizzes': []}

    for quiz in quizzes:
        from app.api.utils import get_quiz
        resp['quizzes'].append(get_quiz(quiz))
    return jsonify(resp)


@api.route('/quiz', methods=['POST'])
@login_required
def upload_quiz_result():
    uid = current_user.get_id()
    db = get_db()
    data = request.get_json()
    is_corrected = data.get('is_corrected')
    question_list = data.get('question_arr')
    answer_list = data.get('answer_arr')
    correct_list = data.get('correct_arr')
    from bson import timestamp
    date = data.get('date')
    date = timestamp.Timestamp(date // 1000, 1)
    time_used = data.get('time_used')
    category = str(data.get('category'))
    quiz = dict()
    quiz['uid'] = uid
    quiz['date'] = date
    quiz['time_used'] = time_used
    quiz['category'] = category
    quiz['question_list'] = []
    for i in range(len(question_list)):
        quiz['question_list'].append({'qid': question_list[i],
                                    'answer': answer_list[i],
                                    'score': correct_list[i] if is_corrected else -1
                                    })
    result = db.quiz.insert_one(quiz)
    resp = dict()
    resp['_id'] = str(result.inserted_id)
    return jsonify(resp)


@api.route('/quiz/<string:quiz_id>', methods=['GET'])
@login_required
def get_quiz_by_id(quiz_id: str):
    uid = current_user.get_id()
    db = get_db()
    quiz_id = ObjectId(quiz_id)
    quiz = db.quiz.find_one({'_id': quiz_id})
    if not quiz:
        abort(404)
    from app.api.utils import get_quiz
    return jsonify(get_quiz(quiz))


@api.route('/quiz/generate/<int:question_num>/<string:category>', methods=['GET'])
@login_required
def generate_quiz(question_num: int, category: str):
    uid = current_user.get_id()
    query = {"uid": uid, "category": category}
    questions = get_all_question(query)
    questions = random.sample(list(questions), min(len(list(questions)), question_num))
    resp = transfer_question_dict(questions)
    return jsonify(resp)
