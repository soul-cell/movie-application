from movie_application.database import db_details
from fastapi import APIRouter
import pydantic
from typing import Dict
from models.movie_model import movie
from bson.objectid import ObjectId

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

new_app = APIRouter()


@new_app.get('/')
def get_all_movie():
    data = db_details.movies_collection.find()
    return list(data)


@new_app.post('/search')
def post_movie(values: Dict):
    data = db_details.movies_collection.find(values)
    return list(data)


@new_app.delete("/")
async def delete_movie(value: Dict):
    db_details.movies_collection.find_one_and_delete(value)
    return {"data": []}


@new_app.post("/")
async def post_data(info: movie):
    data = info.dict()
    db_details.movies_collection.insert_one(data)
    return "data successfully inserted"


@new_app.put("/")
async def update_movie(movie_id: str, value: Dict):
    query = {"_id": ObjectId(movie_id)}
    update = {"$set": value}
    db_details.movies_collection.update_one(query, update)
    return "sucessfully updated"


@new_app.delete("/{id}")
async def delete_movie(id: str):
    db_details.movies_collection.find_one_and_delete({"_id": ObjectId(id)})
    return "Successfully deleted"
