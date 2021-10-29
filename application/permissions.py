from functools import wraps

from flask_jwt_extended import current_user
from flask import abort


class permission_required:
    def __init__(self, instance):
        self.instance = instance

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            instance = self.instance.query.get(kwargs['instance_id'])
            if not current_user or (not current_user.is_admin and current_user.id != instance.author_id):
                abort(403, 'Permissions denied')
            return func(*args, **kwargs)

        return decorated
