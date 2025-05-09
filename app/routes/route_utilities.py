from ..db import db
from flask import abort, make_response
from app.models.task import Task


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model_from_dict(cls, task_data):
    try: 
        new_instance = cls.from_dict(task_data)
    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    db.session.add(new_instance)
    db.session.commit()
    model_name = cls.__name__.lower() 
    
    return {model_name: new_instance.to_dict()}, 201


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    sort_order = None
    if filters:
        # Pull out 'sort' and prevent it from becoming a filter
        sort_order = filters.get("sort", None)

        # Apply other filters
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    # Apply sorting
    if sort_order == "asc":
        query = query.order_by(cls.title.asc())
    elif sort_order == "desc":
        query = query.order_by(cls.title.desc())
    else:
        query = query.order_by(cls.id)

    models = db.session.scalars(query)
    return [model.to_dict() for model in models]


def assign_tasks(goal, task_ids):
    # Clear current tasks
    for task in goal.tasks:
        task.goal_id = None

    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
        tasks.append(task)

    return tasks