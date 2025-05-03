from ..db import db
from flask import abort, make_response

def validate_model(cls, model.id):
    try:
        model.id = int(model.id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response , 400))

        query = db.select(cls).where(cls.id == model_id)
        model = db.session.scalar(query)# odin object 
        
        if not model:
            response = {"message": f"{cls.__name__} {model_id} not found"}
            abort(make_response(response, 404))
        
        return model