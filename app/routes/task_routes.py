from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app import db
from .route_utilities import create_model_from_dict
from .route_utilities import validate_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks") # main rout

# create task
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()  
    return create_model_from_dict(Task, request_body)

# get all books
@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    
    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))
        
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))
    
    is_complete_param = request.args.get("is_complete")
    if is_complete_param:
        query = query.where(Task.completed_at.isnot(None if is_complete_param == True else True))
    
    tasks = db.session.scalars(query.order_by(Task.id))
    
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

# get one task
@tasks_bp.get("/<task_id>")
def get_one_book(task_id):
    task = validate_model(Task, task_id)
    
    return task.to_dict()