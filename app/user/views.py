import json
import requests
from flask import Blueprint, request, jsonify, session, current_app
from app.db import get_db

user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
def get_user_info():
    code = request.args.get('code')
    appid = current_app.config['APPID']
    secret = current_app.config['SECRET']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' \
          % (appid, secret, code)
    r = requests.get(url)
    result = json.loads(r.text)
    if not result.get('errcode'):
        openid = result.get('openid')
        session_key = result.get('session_key')
        db = get_db()
        u = db.user.find_one({'openid': openid})
        if not u:
            db.user.insert_one({
                'openid': openid,
                'session_key': session_key
            })
        return jsonify({'token': openid})
    print(result)
    return result
