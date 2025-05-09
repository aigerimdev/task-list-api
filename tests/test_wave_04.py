# There are no tests for wave 4.
from unittest.mock import patch
from app.models.task import Task
from app.db import db

def test_mark_complete_on_incomplete_task(client, one_task):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        response = client.patch("/tasks/1/mark_complete")
    assert response.status_code == 204
    task = db.session.scalar(db.select(Task).where(Task.id == 1))
    assert task.completed_at

def test_mark_incomplete_on_complete_task(client, completed_task):
    response = client.patch("/tasks/1/mark_incomplete")
    assert response.status_code == 204
    task = db.session.scalar(db.select(Task).where(Task.id == 1))
    assert task.completed_at is None

def test_mark_complete_on_completed_task(client, completed_task):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        response = client.patch("/tasks/1/mark_complete")
    assert response.status_code == 204
    task = db.session.scalar(db.select(Task).where(Task.id == 1))
    assert task.completed_at

def test_mark_incomplete_on_incomplete_task(client, one_task):
    response = client.patch("/tasks/1/mark_incomplete")
    assert response.status_code == 204
    task = db.session.scalar(db.select(Task).where(Task.id == 1))
    assert task.completed_at is None

def test_mark_complete_missing_task(client):
    response = client.patch("/tasks/1/mark_complete")
    assert response.status_code == 404
    assert response.get_json() == {"message": "Task 1 not found"}

def test_mark_incomplete_missing_task(client):
    response = client.patch("/tasks/1/mark_incomplete")
    assert response.status_code == 404
    assert response.get_json() == {"message": "Task 1 not found"}
