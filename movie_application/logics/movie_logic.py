from movie_application.database import db_initialization
from fastapi import APIRouter
from pydantic import json
from typing import Dict
from movie_application.models.movie_model import Movie
from bson.objectid import ObjectId

json.ENCODERS_BY_TYPE[ObjectId] = str

new_app = APIRouter()


@new_app.post('/search')
def read_movie(values: Dict):
    data = list(db_initialization.movies_collection.find(values))
    return data


@new_app.post('/insert')
def insert_movie(info: Movie):
    data = info.dict()
    result = db_initialization.movies_collection.insert_one(data)
    if result:
        data_get = read_movie({"_id": result.inserted_id})
        return data_get
    else:
        return "insertion failed"


@new_app.put("/")
def update_movie(movie_id: str, value: Dict):
    query = {"_id": ObjectId(movie_id)}
    update = {"$set": value}
    data = db_initialization.movies_collection.find_one_and_update(query, update, return_document=True)
    if data:
        return data
    else:
        return "updating failed"


non_deleted = []
id_list = []


@new_app.delete("/")
def delete_movie(ids: list):
    for i in ids:
        result = db_initialization.movies_collection.find_one_and_delete({"_id": ObjectId(i)})
        if result:
            id_list.append(i)
        else:
            non_deleted.append(i)
    if non_deleted:
        return "non deleted ids:", non_deleted, "deleted ids:", id_list

    else:
        return f"successfully deleted and deleted ids are{id_list} non deleted ids are{non_deleted}"
