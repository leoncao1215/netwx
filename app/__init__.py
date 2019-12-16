import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from config import DevelopmentConfig
    app.config.from_object(DevelopmentConfig())

    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/login')

    from .user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # from . import db
    # db.init_app(app)

    return app
