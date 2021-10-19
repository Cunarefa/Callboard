import datetime
import os

import pytest
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import close_all_sessions

from application import create_app, db
from application.models import User
from application.models import Post


@pytest.fixture
def client():
    _app = create_app()
    _app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_SQLALCHEMY_DATABASE_URI')
    client = _app.test_client()

    with _app.app_context():
        db.create_all()

        yield client

        close_all_sessions()
        db.drop_all()


@pytest.fixture
def user():
    user = User(
        username="testuser",
        password="12345",
        email="aldo@mail.ru"
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def post(user):
    post = Post(title='My post', author_id=user.id)
    db.session.add(post)
    db.session.commit()
    return post


@pytest.fixture
def headers(user):
    access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(days=1))
    return {'Authorization': 'Bearer {}'.format(access_token)}
