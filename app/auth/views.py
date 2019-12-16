from flask import Blueprint, request, jsonify, session
from app.db import get_db
auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST'])
def login():
    wx_id = request.form.get('wx_id', type=int)
    if wx_id:
        db = get_db()
        user = db.user.find_one({'wx_id': wx_id})
        if not user:
            db.user.insert_one({'wx_id': wx_id})
        session['wx_id'] = wx_id
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed', 'message': 'Need wx_id!'})
