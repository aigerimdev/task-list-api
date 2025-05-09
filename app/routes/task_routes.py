from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app import db
from .route_utilities import create_model_from_dict
from .route_utilities import validate_model, get_models_with_filters
from datetime import datetime, UTC
from dotenv import load_dotenv
import requests
import os

load_dotenv()


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks") # main rout

# create task
@bp.post("")
def create_task():
    task_data = request.get_json()  
    return create_model_from_dict(Task, task_data)

# get all tasks
@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

# get one task
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict(include_goal_id=(task.goal_id is not None))}


# update task
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

# delete task
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

def notify_slack(task_title):
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": SLACK_CHANNEL,
        "text": f"Someone just completed the task {task_title}"
    }
    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
    return response.json()

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at is None:
        task.completed_at = datetime.now(UTC)
        db.session.commit()
        notify_slack(task.title)

    return Response(status=204, mimetype="application/json")


# partially update incompleted
@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")
