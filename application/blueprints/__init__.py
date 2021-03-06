from flask import Blueprint

auth_api = Blueprint('auth_api', __name__)
user_api = Blueprint('user_api', __name__)
post_api = Blueprint('post_api', __name__)
comment_api = Blueprint('comment_api', __name__)
like_api = Blueprint('like_api', __name__)

from application.blueprints import auth, users, posts, comments, likes
