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
    result = db_initialization.users_collection.insert_one(data)
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


def find_average(movie_id, new_rating, function):
    x = list(
        db_initialization.movies_collection.find({"_id": ObjectId(movie_id)}, {"_id": False, "overall_ratings": True}))
    x1 = list(x[0]["overall_ratings"].keys())
    x2 = list(x[0]["overall_ratings"].values())

    if function == "remove":
        new_avg = ((x2[0] * float(x1[0])) - new_rating) / (x2[0] - 1)
        if new_avg >= 60:
            query = {"$set":{"status": "hit", "overall_ratings": {str(new_avg): x2[0] - 1}}}
            db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
            return "success"
        else:
            query = {"$set":{"status": "flop", "overall_ratings": {str(new_avg): x2[0] - 1}}}
            db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
            return "success"

    if function == "add":
        new_avg = ((x2[0] * float(x1[0])) + new_rating) / (x2[0] + 1)
        if new_avg >= 60:
            query = {"$set": {"status": "hit", "overall_ratings": {str(new_avg): x2[0] + 1}}}

            db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
            return "success"
        else:
            query = {"$set": {"status": "flop", "overall_ratings": {str(new_avg): x2[0] + 1}}}
            db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
            return "success"


print(find_average("6487088522fbe63afc2aafb2", 65, function="remove"))
