from fastapi import HTTPException
from bson.objectid import ObjectId

def validate_object_id(id):
    try:
        _id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Id invalid")
    return _id