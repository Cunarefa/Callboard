import datetime

from marshmallow import EXCLUDE, fields, validate

from application import db, ma
from application.models.likes import likes


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.date.today())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    type = db.Column(db.String(255))
    priority = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('User', secondary=likes, backref='liked', lazy='dynamic')

    def __str__(self):
        return self.title


class PostSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    title = fields.String(validate=validate.Length(max=255))
    description = fields.String(validate=validate.Length(max=500))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    type = fields.String(validate=validate.Length(max=255))
    priority = fields.Integer()
    author_id = fields.Integer(dump_only=True)
