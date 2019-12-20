from flask_login.login_manager import LoginManager
from .views import auth as auth_blueprint
from app.db import get_db
from app.user.models import User

login_manager = LoginManager()


def init_app(app):
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    res = db.user.find_one({'openid': user_id})
    if res:
        user = User(res['openid'])
        return user
    return None


@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        db = get_db()
        res = db.user.find_one({'openid': api_key})
        if res:
            user = User(res.get('openid'))
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    print(api_key)
    if api_key:
        db = get_db()
        # api_key = api_key.replace('Basic ', '', 1)
        # try:
        #     import base64
        #     api_key = base64.b64decode(api_key).decode('utf-8')
        #     print(api_key)
        # except TypeError:
        #     pass
        res = db.user.find_one({'openid': api_key})
        print(res)
        if res:
            user = User(res.get('openid'))
            return user

    # finally, return None if both methods did not login the user
    return None



