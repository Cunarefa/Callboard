from application import db


likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                 db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                 )
