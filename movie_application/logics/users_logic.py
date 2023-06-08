from movie_application.database import db_details
from fastapi import APIRouter
import pydantic
from typing import Dict

from bson.objectid import ObjectId

pydantic.json.ENCODERS_BY_TYPE[ObjectId]= str

new_app = APIRouter()

@new_app.get('/')
def get_all_users():
    data= db_details.users_collection.find()
    return list(data)

@new_app.post('/search the user')
def post_user(values:Dict):
    data = db_details.users_collection.find(values)
    return list(data)

@new_app.delete("/delete the user")
async def delete_user(value: Dict):
    data = db_details.users_collection.find_one_and_delete(value)
    return {"data": []}
