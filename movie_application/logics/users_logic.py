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
    data = info.dict()
    result = db_initialization.users_collection.insert_one(
        data)  # check if insert operation is successfull befor returning successfull
    if result:
        return "Inserted successfully"
    else:
        return "Insertion failed"


# update a user

@user_app.put("/")
def update_user(user_id: str, value: Dict):
    query = {"_id": ObjectId(user_id)}
    update = {"$set": value}
    data = db_initialization.users_collection.update_one(query, update)
    if data.modified_count > 0:
        return "Updated user info Successfully !!"
    else:
        return "Failed to Update"


# delete a specific user

non_deleted = []
id_list = []


@user_app.delete("/")
def delete_user(ids: list):
    for j in ids:
        result = db_initialization.users_collection.find_one_and_delete({"_id": ObjectId(j)})
        if result:
            id_list.append(j)
        else:
            non_deleted.append(j)
    if non_deleted:
        return non_deleted
    else:
        return "Deleted the User Successfully !"
