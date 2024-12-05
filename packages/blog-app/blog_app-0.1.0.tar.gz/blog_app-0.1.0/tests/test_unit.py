import pytest
from ..app import app
from ..database import db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client_test:
        with app.app_context():
            db.create_all()
            yield client_test
            db.drop_all()


def test_create_new_post(client):
    """Test creating a new blog post"""
    # Create a test post
    test_content = "This is a test post"
    response = client.post('/posts', json={'content': test_content})

    # Verify response status
    assert response.status_code == 201

    # Verify response data
    data = response.get_json()
    assert data['content'] == test_content
    assert 'id' in data
    assert 'created_at' in data

    # Verify post was saved in database
    response = client.get('/posts')
    posts = response.get_json()
    assert len(posts) == 1
    assert posts[0]['content'] == test_content