from flask import Blueprint, request, Response
from app.models.task import Task
from app.models.goal import Goal
from app import db
from .route_utilities import validate_model, get_models_with_filters, create_model_from_dict, assign_tasks
import requests
import os

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# create goal
@bp.post("")
def create_goal():
    goal_data = request.get_json()
    return create_model_from_dict(Goal, goal_data)

# get all goals
@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

# get one goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {"goal": goal.to_dict()}
    
# update goal
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    goal.title = request_body["title"]
    
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

# delete goal
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

# nested routes
@bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])
    
    tasks = assign_tasks(goal, task_ids)
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }, 200


@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict(include_goal_id=True) for task in goal.tasks]
    }, 200