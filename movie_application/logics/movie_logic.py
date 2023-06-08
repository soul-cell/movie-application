from movie_application.database import db_details
from fastapi import APIRouter
import pydantic

from bson.objectid import ObjectId

pydantic.json.ENCODERS_BY_TYPE[ObjectId]= str

new_app = APIRouter()


@new_app.get('/')
def get_all_movie():
    data = database.mycollection.find()
    return list(data)


@new_app.post("/")
async def get_one_movie(values: Dict):
    data = database.mycollection.find(values)
    return data

@new_app.delete("/")
async def delete_movie(value: Dict):
    database.mycollection.find_one_and_delete(value)
    return {"data": []}
