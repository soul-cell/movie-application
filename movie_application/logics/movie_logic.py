from movie_application.database import db_details
from fastapi import APIRouter
import pydantic
from typing import Dict

from bson.objectid import ObjectId

pydantic.json.ENCODERS_BY_TYPE[ObjectId]= str

new_app = APIRouter()

@new_app.get('/')
def get_all_movie():
    data=db_details.movies_collection.find()
    return list(data)

@new_app.post('/search')
def post_movie(values:Dict):
    data = db_details.movies_collection.find(values)
    return list(data)

@new_app.delete("/")
async def delete_movie(value: Dict):
    db_details.movies_collection.find_one_and_delete(value)
    return {"data": []}
