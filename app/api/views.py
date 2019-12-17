from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from app.db import get_db

api = Blueprint('api', __name__)


# 获取错题列表, 默认不包括不重要的
@api.route('/wqs', methods=['GET'])
@login_required
def get_wrong_questions():
    dismissed = request.args.get('dismissed', default=False, type=bool)
    category = request.args.get('category', default=None, type=str)
    uid = current_user.get_id()
    db = get_db()
    query = {"uid": uid, "dismissed": dismissed}
    if category:
        query['category'] = category
    questions = db.question.find(query)

    resp = {
        "questions": [
            {
                '_id': str(q['_id']),
                'description': q['description'],
                'answer': q['answer'],
                'date': q['date'].time
            } for q in questions
        ]
    }
    return jsonify(resp)


@api.route('/wqs', methods=['POST', 'PUT'])
@login_required
def update_wrong_questions():
    from bson import ObjectId, timestamp
    uid = current_user.get_id()
    db = get_db()
    resp = {}

    f = request.files['file']
    if f:  # upload picture question
        ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])  # 允许上传的文件类型
        def allowed_file(filename):  # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
            return '.' in filename and \
                   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        from gridfs import GridFS

        fname = f.filename
        if allowed_file(fname):
            gfs = GridFS(db, collection = 'question')
            fparts = fname.split('.')
            fdesc = fparts[0] # file name
            ftype = fparts[1] # file extend name

            answer = request.form.get('answer')
            dismissed = (False, True)[request.form.get('dismissed').lower() == 'true']
            category = request.form.get('category')
            if request.method == 'PUT': # delete original picture
                _id = request.form.get('_id')
                obj_id = ObjectId(_id)
                condition = {'uid': uid, '_id': obj_id}
                result = gfs.find_one(condition)  # check uid
                if not result:
                    resp['status'] = 'Failed'
                    resp['message'] = '_id not found'
                    return jsonify(resp)
                else:
                    gfs.delete(obj_id)

            insertimg = gfs.put(f, content_type = ftype, filename = fdesc,
                                uid = uid, answer = answer, dismissed = dismissed, category = category)
            resp['_id'] = str(insertimg)
            return jsonify(resp)
    else: # upload text question
        def load_request_attr(question, request):
            question_attrs = ['description', 'answer', 'dismissed', 'category', 'date']
            for attr_name in question_attrs:
                attr = request.json.get(attr_name)
                if attr_name == 'date':
                    attr = timestamp.Timestamp(attr, 1)
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


@api.route('/quiz/<bool:is_corrected', methods=['POST'])
@login_required
def upload_quiz_result(is_corrected: bool):
    uid = current_user.get_id()
    db = get_db()
    data = request.get_json()
    question_list = data.get('question_arr')
    answer_list = data.get('answer_arr')
    correct_list = data.get('correct_arr')
    from bson import timestamp
    date = data.get('date')
    date = timestamp.Timestamp(date, 1)
    time_used = data.get('time_used')
    quiz = dict()
    quiz['uid'] = uid
    quiz['date'] = date
    quiz['time_used'] = time_used
    quiz['question_list'] = []
    for i in range(len(question_list)):
        quiz['question_list'][i] = {'qid': question_list[i],
                                    'answer': answer_list[i],
                                    'score': -1 if is_corrected else correct_list[i]
                                    }
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
    db = get_db()
    query = {"uid": uid, "category": category}
    questions = db.question.find(query)
