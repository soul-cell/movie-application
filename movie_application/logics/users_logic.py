from movie_application.database import db_initialization
from fastapi import APIRouter
import pydantic
from typing import Dict

from bson.objectid import ObjectId

from movie_application.models.users_model import User

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

new_app = APIRouter()


@new_app.get('/')
def get_all_users():
    data = db_initialization.users_collection.find()
    return list(data)


@new_app.post('/search the user')
def create_user(values: Dict):
    data = db_initialization.users_collection.find(values)
    return list(data)


@new_app.delete("/delete the user")
async def delete_user(value: Dict):
    data = db_initialization.users_collection.find_one_and_delete(value)
    return {"data": []}


@new_app.post("/new")
async def post_data(info: User):
    data = info.dict()
    db_initialization.users_collection.insert_many(data)
    return "Inserted New User !"


# delete a specific user

@new_app.delete("/{id}")
async def delete_user(id: str):
    db_initialization.users_collection.find_one_and_delete({"_id": ObjectId(id)})
    return "Deleted Succesfully !"


# insert a user
@new_app.post("/insert")
async def post_data(info: User):
    data = info.dict()
    db_initialization.users_collection.insert_one(data)
    return "Inserted Successfully !"


# update a user

@new_app.put("/Update")
def update_user(user_id: str, value: Dict):
    query = {"_id": ObjectId(user_id)}
    update = {"$set": value}
    db_initialization.users_collection.update_many(query, update)
    return "Updated Successfully !"

@new_app.post("/")
def insert_user(info: User):
    data = info.dict()
    result = db_initialization.users_collection.insert_one(data)
    if result:
        return "Instered user Successfully !"
    else:
        return "Failed to insert"

#update

@new_app.put("/")
def update_user(user_id: str, value: Dict):
    query = {"_id": ObjectId(user_id)}
    update = {"$set": value}
    data = db_initialization.users_collection.update_one(query,update)
    if data.modified_count > 0:
        return "Updated user info Successfully !!"
    else:
        return "Failed to update"