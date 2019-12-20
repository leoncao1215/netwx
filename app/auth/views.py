import requests
import json
from flask import Blueprint, request, jsonify, current_app, abort
from flask_login import login_user, logout_user, login_required
from app.db import get_db
from app.user.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    code = json.loads(request.data).get('code')
    if not code:
        abort(400)
    appid = current_app.config['APPID']
    secret = current_app.config['SECRET']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' \
          % (appid, secret, code)
    r = requests.get(url)
    result = json.loads(r.text)
    errcode = result.get('errcode')
    if not errcode:
        openid = result.get('openid')
        session_key = result.get('session_key')
        db = get_db()
        u = db.user.find_one({'openid': openid})
        if not u:
            u = db.user.insert_one({
                'openid': openid,
                'session_key': session_key
            })
        user = User()
        user.id = u.get('openid')
        login_user(user)
        return jsonify({'status': 'success', 'message': 'Login'})
    else:
        print(result)
        if errcode == 40029:
            return jsonify({'status': 'failed', 'message': 'code 无效'})
        elif errcode == 45011:
            return jsonify({'status': 'failed', 'message': '达到频率限制'})
        elif errcode == -1:
            return jsonify({'status': 'failed', 'message': '系统繁忙，请稍候再试'})
    # wx_id = request.form.get('wx_id', type=str)
    # if wx_id:
    #     db = get_db()
    #     res = db.user.find_one({'wx_id': wx_id})
    #     if not res:
    #         res = db.user.insert_one({'wx_id': wx_id})
    #     user = User()
    #     user.id = res.get('wx_id')
    #     login_user(user)
    #     return jsonify({'status': 'success', 'message': 'Login'})
    # else:
    #     return jsonify({'status': 'failed', 'message': 'Need wx_id!'})


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': 'Logout'})
