import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    from application import models

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    migrate.init_app(app, db)

    from application.blueprints import auth_api, user_api, post_api

    app.register_blueprint(auth_api, url_prefix='/api')
    app.register_blueprint(user_api, url_prefix='/api')
    app.register_blueprint(post_api, url_prefix='/api')

    return app