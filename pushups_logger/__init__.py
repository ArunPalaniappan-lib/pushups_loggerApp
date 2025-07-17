# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)

#     app.config['SECRET_KEY'] = 'secret-key-goes-here'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

#     db.init_app(app)

#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     from .auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)

#     return app

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'db.sqlite')

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
