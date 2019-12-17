from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.db import get_db
api = Blueprint('api', __name__)


# 获取错题列表, 默认不包括不重要的
@api.route('/wqs', methods=['GET'])
@login_required
def get_wrong_questions():
    dismissed = request.args.get('dismissed', default=False, type=bool)
    category  = request.args.get('category',  default=None,  type=str)
    uid = current_user.get_id()
    db = get_db()
    query = {"uid": uid, "dismissed": dismissed}
    if category:
        query['category'] = category
    questions = db.question.find(query)

    resp = {"questions": [{
        'id'        : q['id'],
        'question'  : q['question']
    } for q in questions]}
    return jsonify(resp)


@api.route('/wqs', methods=['POST', 'PUT'])
def update_wrong_questions():
    if request.method == 'POST':
        # 上传错题
        pass
    else:
        # 更新错题
        pass


@api.route('/wqs/<int:wq_id>', methods=['DELETE'])
def delete_wrong_question(wq_id: int):
    pass


@api.route('/wqs/categories', methods=['GET'])
def get_categories():
    pass


@api.route('/contests', methods=['GET'])
def get_contests():
    pass


@api.route('/contests', methods=['POST'])
def upload_contest_result():
    pass


@api.route('/contests/<int:contest_id>', methods=['GET'])
def get_contest_by_id(contest_id: int):
    pass


@api.route('/contests/generate', methods=['GET'])
def generate_contest():
    pass

