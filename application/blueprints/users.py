from application.blueprints import user_api
from application.models import User
from application.models.users import UserSchema


@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    schema = UserSchema()
    return schema.dump(user)