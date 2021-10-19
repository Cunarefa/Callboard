import datetime

from marshmallow import fields, validate

from application import db, ma


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.date.today())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


class CommentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String(validate=validate.Length(max=1000))
    created_at = fields.DateTime(dump_only=True)
    author_id = fields.Integer(dump_only=True)
    post_id = fields.Integer(dump_only=True)
