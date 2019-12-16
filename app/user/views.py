import requests
from flask import Blueprint, request, jsonify, session, current_app
from app.db import get_db

user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
def get_user_info():
    code = request.data
    appid = current_app.config['APPID']
    secret = current_app.config['SECRET']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' \
          % (appid, secret, code)
    r = requests.get(url)
    result = r.text
    return result
