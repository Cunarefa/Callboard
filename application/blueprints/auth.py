import datetime

from flask import request, abort, make_response
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from application import db
from application.blueprints import auth_api
from application.models import User
from application.models.users import UserSchema


@auth_api.route('/register', methods=["POST"])
def register():
    json_data = request.json

    schema = UserSchema()
    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    data['password'] = generate_password_hash(data['password'])
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(days=1))
    return {"user": schema.dump(user), "token": token}


@auth_api.route('/login', methods=['GET'])
def login():
    json_data = request.json

    schema = UserSchema()
    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    username = data['username']
    password = data['password']

    user = User.query.filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=user.username)
        return {"user": schema.dump(user), "token": token}
    return make_response("Wrong username or password", 401)
