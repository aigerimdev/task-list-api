from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from flask import jsonify

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

#create task
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
    except KeyError as err:
        response = {"message": f"Invalid request: missing {err.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task": new_task.to_dict()}), 201
