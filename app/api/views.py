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
    question_attrs = ['description', 'answer', 'dismissed', 'category', 'date']
    question = {'uid': uid}
    for attr_name in question_attrs:
        question[attr_name] = request.json.get(attr_name)
    print(question)
    db = get_db()
    if request.method == 'POST':
        # 上传错题
        db.question.insert(question)
    else:
        # 更新错题
        pass
    return 'update_wrong_questions'


@api.route('/wqs/<string:wq_id>', methods=['DELETE'])
@login_required
def delete_wrong_question(wq_id: str):
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
        from app.api.utils import get_quiz
        resp['quizzes'].append(get_quiz(quiz))
    return jsonify(resp)


@api.route('/quiz', methods=['POST'])
@login_required
def upload_quiz_result():
    uid = current_user.get_id()
    pass


@api.route('/quiz/<string:quiz_id>', methods=['GET'])
@login_required
def get_quiz_by_id(quiz_id: str):
    uid = current_user.get_id()
    db = get_db()
    quiz = db.quiz.find_one({'id': quiz_id})
    if not quiz:
        abort(404)
    from app.api.utils import get_quiz
    return jsonify(get_quiz(quiz))
    pass


@api.route('/quiz/generate', methods=['GET'])
@login_required
def generate_quiz():
    uid = current_user.get_id()
    pass
