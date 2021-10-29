from flask import jsonify, abort
from flask_jwt_extended import current_user, jwt_required

from application import db
from application.blueprints import like_api
from application.models import Post
from application.models.likes import likes
from application.models import User
from application.models.posts import PostSchema


@like_api.route('/posts/<int:post_id>/likes', methods=['POST'])
@jwt_required()
def like_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    like = db.session.query(likes).filter(likes.c.user_id == current_user.id, likes.c.post_id == post.id).first()
    if not like:
        current_user.liked_posts.append(post)
        db.session.commit()
        return {"message": f"You just liked post - {post.title}"}


@like_api.route('/posts/<int:post_id>/likes', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    like = db.session.query(likes).filter(likes.c.user_id == current_user.id, likes.c.post_id == post.id).first()
    if like:
        current_user.liked_posts.remove(post)
        db.session.commit()
        return {"message": f"Post - {post.title} was unliked"}


@like_api.route('/users/likes', methods=['GET'])
@jwt_required()
def get_user_liked_posts():
    posts = current_user.liked_posts
    schema = PostSchema(many=True)
    return jsonify(schema.dump(posts))
