from application import db
from application.models.likes import likes


def test_like(client, headers, post, user):
    like = db.session.query(likes).filter(likes.c.user_id == user.id, likes.c.post_id == post.id).first()
    if not like:
        rv = client.post(f'/api/posts/{post.id}/likes', headers=headers)
        assert b"You just liked post - My post" in rv.data


def test_unlike(client, headers, post, user):
    user.liked_posts.append(post)
    like = db.session.query(likes).filter(likes.c.user_id == user.id, likes.c.post_id == post.id).first()
    if like:
        rv = client.delete(f'/api/posts/{post.id}/likes', headers=headers)
        assert b"Post - My post was unliked" in rv.data

