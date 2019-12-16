from flask import Blueprint, request
from app.db import get_db
api = Blueprint('api', __name__)


# 获取错题列表, 默认不包括不重要的
@api.route('/wqs', methods=['GET'])
def get_wrong_questions():
    dismissed = request.args.get('dismissed', default=False, type=bool)
    category  = request.args.get('category',  default=None,  type=str)

    print(dismissed, category)

    # Demo db connection
    db = get_db()
    persons = db.test.find({'name': 'test'})
    resp = ''.join([person['name'] for person in persons])
    return resp


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


@api.route('/contests/generate', methods=['GET'])
def generate_contest():
    pass


@api.route('/contests', methods=['GET'])
def get_contests():
    pass


@api.route('/contests/<int:contest_id', methods=['GET'])
def get_contests(contest_id: int):
    pass


@api.route('/contests', methods=['POST'])
def upload_contest_result():
    pass





