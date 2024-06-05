import pytest
from app import app, db
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL_TESTING')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json == []

def test_add_task(client):
    response = client.post('/tasks', json={'title': 'Test Task'})
    assert response.status_code == 200
    assert response.json['title'] == 'Test Task'

def test_update_task(client):
    response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = response.json['id']

    response = client.put(f'/tasks/{task_id}', json={'completed': True})
    assert response.status_code == 200
    assert response.json['completed'] is True

def test_delete_task(client):
    response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = response.json['id']

    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204

    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) == 0
