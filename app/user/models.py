from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id=None):
        if id:
            self.__user_id = user_id

    @property
    def id(self):
        return self.__user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user_id)

