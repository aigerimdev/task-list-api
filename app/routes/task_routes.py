from flask import Blueprint, abort, make_response, request
from app.models.task import Task
from .route_utilities import create_model_from_dict

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks") # main rout

# create task
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()  
    return create_model_from_dict(Task, request_body)