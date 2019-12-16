import requests
from flask import Blueprint, request, jsonify, session
from app.db import get_db
user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
def get_user_info():
    appid, secret, code = request.data
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appid, secret, code)
    r = requests.get(url)
    result = r.text
    return result
