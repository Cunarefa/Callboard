from application.models import Post


def test_add_comment(client, headers, post):
    json_data = {"content": "I proud of you"}
    client.post('/api/comments/posts/1', json=json_data, headers=headers)
    rv = Post.query.filter(Post.id == post.id).first_or_404().comments.first()

    assert rv.content == "I proud of you"


def test_delete_comment(client, headers, post):
    json_data = {"content": "I proud of you"}
    client.post(f'/api/comments/posts/{post.id}', json=json_data, headers=headers)
    v = Post.query.filter(Post.id == post.id).first_or_404().comments.all()
    assert len(v) == 1

    client.delete('/api/comments/1', headers=headers)
    rv = Post.query.filter(Post.id == post.id).first_or_404().comments.all()
    assert len(rv) == 0


