from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
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
                'id': q['id'],
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
    uid = current_user.get_id()
    if request.method == 'POST':
        # 上传错题
        pass
    else:
        # 更新错题
        pass


@api.route('/wqs/<string:wq_id>', methods=['DELETE'])
@login_required
def delete_wrong_question(wq_id: int):
    uid = current_user.get_id()
    db = get_db()
    q = db.question.find_one({'id': wq_id})
    if not q:
        abort(404)
    db.question.delete_one({'id': wq_id})
    return jsonify({'status': 'Success'})


@api.route('/wqs/categories', methods=['GET'])
@login_required
def get_categories():
    uid = current_user.get_id()
    db = get_db()
    res = db.question.find({'uid': uid})
    categories = set([_['category'] for _ in res])
    resp = {'categories': list(categories)}
    return jsonify(resp)


@api.route('/quiz', methods=['GET'])
@login_required
def get_all_quizzes():
    uid = current_user.get_id()
    db = get_db()
    quizzes = db.quiz.find({'uid': uid})
    resp = {'quizzes': []}

    for quiz in quizzes:
        questions = quiz['question_list']
        print(type(quiz['date']))
        tmp = {
            'id': quiz['id'],
            'date': quiz['date'].time,
            'question_list': [],
            'total_num': len(questions),
            'correct_num': len([q['score'] for q in questions if q['score'] == 1]),
            'timing': sum([q['timing'] for q in questions]),
            'scored': len([q['score'] for q in questions if q['score'] == -1]) == 0
        }
        for q in questions:
            tmp_qes = {
                'qid': q['qid'],
                'description': db.question.find_one({'id': q['qid']}).get('question'),
                'answer': q['answer'],
                'scored': q['score'] != -1,
                'timing': q['timing']
            }
            if q['score'] == 1:
                tmp_qes['is_correct'] = True
            elif q['score'] == 0:
                tmp_qes['is_correct'] = False
            tmp['question_list'].append(tmp_qes)

        resp['quizzes'].append(tmp)
    return jsonify(resp)


@api.route('/quiz', methods=['POST'])
@login_required
def upload_quiz_result():
    uid = current_user.get_id()
    pass


@api.route('/quiz/<int:contest_id>', methods=['GET'])
@login_required
def get_quiz_by_id(contest_id: int):
    uid = current_user.get_id()
    pass


@api.route('/quiz/generate', methods=['GET'])
@login_required
def generate_quiz():
    uid = current_user.get_id()
    pass
