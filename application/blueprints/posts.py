from flask import request, abort, jsonify
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from application import db
from application.blueprints import post_api
from application.models.posts import PostSchema, Post
from application.models import User
from application.permissions import permission_required


@post_api.route('/posts', methods=['POST'])
@jwt_required()
@permission_required(Post)
def create_post():
    json_data = request.json

    schema = PostSchema()
    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    data['author_id'] = current_user.id
    post = Post(**data)
    db.session.add(post)
    db.session.commit()
    return schema.dump(post), 201


@post_api.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
@permission_required(Post)
def delete_post(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return {"message": f"Post with {post_id} id deleted"}, 204


@post_api.route('/posts/<int:post_id>', methods=['PATCH'])
@jwt_required()
@permission_required(Post)
def update_post(post_id):
    json_data = request.json

    post = db.session.query(Post).filter(Post.id == post_id).first_or_404()
    schema = PostSchema()
    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    db.session.query(Post).filter(Post.id == post.id).update(data)
    db.session.add(post)
    db.session.commit()
    return schema.dump(post)


@post_api.route('/users/<int:user_id>/posts', methods=['GET'])
def user_posts(user_id):
    posts = db.session.query(Post).join(User, User.id == Post.author_id).filter(User.id == user_id)

    priority = request.args.get('priority')
    post_type = request.args.get('type')
    page = request.args.get('page')

    if post_type:
        posts = posts.filter(Post.type == post_type)
    if priority:
        posts = posts.filter(Post.priority == priority)
    if page:
        posts = posts.paginate(page, 5, False).items

    schema = PostSchema(many=True)
    return jsonify(schema.dump(posts))


@post_api.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first_or_404()
    schema = PostSchema()
    return schema.dump(post), 200
