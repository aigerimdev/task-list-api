from ..db import db
from flask import abort, make_response

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


def create_model_from_dict(cls, data):
    try: 
        new_instance = cls.from_dict(data)
    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    db.session.add(new_instance)
    db.session.commit()
    
    return {"task": new_instance.to_dict()}, 201

