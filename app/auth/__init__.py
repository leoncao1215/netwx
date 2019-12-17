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
    res = db.user.find_one({'wx_id': user_id})
    if res:
        user = User()
        user.id = res['wx_id']
        return user
    return None



