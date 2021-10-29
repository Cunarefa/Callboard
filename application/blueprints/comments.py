from flask import request, abort, jsonify
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from application import db
from application.blueprints import comment_api
from application.models.comments import CommentSchema, Comment
from application.models import Post
from application.permissions import permission_required


@comment_api.route('/comments/posts/<int:post_id>', methods=["POST"])
@jwt_required()
def add_comment(post_id):
    json_data = request.json
    comment_schema = CommentSchema()

    try:
        data = comment_schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    data['author_id'] = current_user.id
    data['post_id'] = post_id
    comment = Comment(**data)
    db.session.add(comment)
    db.session.commit()

    return {"comment": data['content']}


@comment_api.route('/comments/<int:instance_id>', methods=["DELETE"])
@jwt_required()
@permission_required(Comment)
def delete_comment(instance_id):
    comment = Comment.query.filter(Comment.id == instance_id).first_or_404()

    db.session.delete(comment)
    db.session.commit()
    return {'message': f'Comment with {comment.id} successfully deleted'}, 200


@comment_api.route('/comments/<int:instance_id>', methods=["PATCH"])
@jwt_required()
@permission_required(Comment)
def update_comment(instance_id):
    comment = Comment.query.filter(Comment.id == instance_id).first_or_404()
    schema = CommentSchema()

    json_data = request.json
    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    db.session.query(Comment).filter(Comment.id == instance_id).update(data)
    db.session.commit()
    return schema.dump(comment)


@comment_api.route('/posts/<int:post_id>/comments', methods=["GET"])
def post_comments(post_id):
    schema = CommentSchema(many=True)
    comments = Post.query.filter(Post.id == post_id).first_or_404().comments.all()
    return {f"Post {post_id} comments": schema.dump(comments)}


@comment_api.route('/users/comments', methods=['GET'])
@jwt_required()
def user_comments():
    comments = current_user.comments
    schema = CommentSchema(many=True)
    return jsonify(schema.dump(comments))












