from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required
from app.db import get_db
from app.user.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    wx_id = request.form.get('wx_id', type=str)
    if wx_id:
        db = get_db()
        res = db.user.find_one({'wx_id': wx_id})
        if not res:
            res = db.user.insert_one({'wx_id': wx_id})
        user = User()
        user.id = res.get('wx_id')
        login_user(user)
        return jsonify({'status': 'success', 'message': 'Login'})
    else:
        return jsonify({'status': 'failed', 'message': 'Need wx_id!'})


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': 'Logout'})
