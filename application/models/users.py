from marshmallow import EXCLUDE, fields, validate

from application import db, ma, jwt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy='select')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    username = fields.String(validate=validate.Length(min=3))
    email = fields.Email(validate=validate.Length(max=255))
    password = fields.String(validate=validate.Length(max=128), load_only=True)
    first_name = fields.String(validate=validate.Length(max=255))
    last_name = fields.String(validate=validate.Length(max=255))


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()
