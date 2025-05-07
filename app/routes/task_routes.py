from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app import db
from .route_utilities import create_model_from_dict
from .route_utilities import validate_model
from datetime import datetime


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks") # main rout

# create task
@tasks_bp.post("")
def create_task():
    task_data = request.get_json()  
    return create_model_from_dict(Task, task_data)

# get all tasks
@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    
    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)
        
    tasks = db.session.scalars(query)
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

# get one task
@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return {"task": task.to_dict()}

# update task
@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

# delete task
@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    return Response(status=204, mimetype="application/json")