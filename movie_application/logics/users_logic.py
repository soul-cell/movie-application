from movie_application.database import db_initialization
from fastapi import APIRouter
import pydantic
from typing import Dict

from bson.objectid import ObjectId

from movie_application.models.users_model import User

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

user_app = APIRouter()


# search a user

@user_app.post('/search')
def read_user(value: Dict):
    data = db_initialization.users_collection.find(value)
    return list(data)


# insert a user
@user_app.post("/insert")
def insert_user(info: User):  # todo change the function name
    for movie in data['watched_movies']:
        movie_data = read_movie({"_id": ObjectId(movie)})
        if not movie_data:
            return f"movie doesnt exist{movie}"
    # data = info.dict()
    # result = db_initialization.users_collection.insert_one(
    #     data)  # check if insert operation is successfull before returning successfull
    # if result:
    #     get_data = read_user({"_id": result.inserted_id})
    #     return get_data
    # else:
    #     return "Insertion failed"
    data = info.dict()
    result = db_initialization.users_collection.insert_one(
        data)  # check if insert operation is successfull befor returning successfull
    if result:
        get_data = read_user({"_id": result.inserted_id})
        return get_data
    else:
        return "Insertion failed"


# update a user

@user_app.put("/")
def update_user(user_id: str, value: Dict):
    query = {"_id": ObjectId(user_id)}
    update = {"$set": value}
    data = db_initialization.users_collection.find_one_and_update(query, update, return_document=True)
    if data:
        return data
    else:
        return "Failed to Update"


# delete a specific user

@user_app.delete("/")
def delete_user(ids: list):
    non_deleted = []
    id_list = []
    for j in ids:
        result = db_initialization.users_collection.find_one_and_delete({"_id": ObjectId(j)})
        if result:
            id_list.append(j)
        else:
            non_deleted.append(j)
    if non_deleted:
        return "non deleted ids:", non_deleted, "deleted ids:", id_list
    else:
        return f"successfully deleted and deleted ids are{id_list} non deleted ids are{non_deleted}"
