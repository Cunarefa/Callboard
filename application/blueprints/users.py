from flask import abort, jsonify
from flask_jwt_extended import jwt_required, current_user

from application import db
from application.blueprints import user_api
from application.models import User
from application.models.users import UserSchema


@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    schema = UserSchema()
    user = User.query.filter(User.id == user_id).first_or_404()
    if user.deleted:
        abort(404)
    return schema.dump(user)


@user_api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    if user.deleted:
        abort(404)
    if current_user.id != user.id:
        abort(401)

    user.deleted = True
    db.session.commit()
    return {"message": f"User with {user.id} id successfully deleted"}, 200


@user_api.route('/users', methods=['GET'])
def get_all_users():
    schema = UserSchema(many=True)
    users = User.query.filter(User.deleted is not True).all()
    return jsonify({'users': schema.dump(users)})



