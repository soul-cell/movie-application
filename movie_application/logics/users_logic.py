import movie_application.logics.movie_logic
from movie_application.database import db_initialization
from fastapi import APIRouter, HTTPException
import pydantic
from typing import Dict

from bson.objectid import ObjectId
from movie_application.models.users_model import User

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

user_app = APIRouter()


# search a user

@user_app.post('/search')
def read_user(value: Dict):
    if "_id" in value.keys():
        value["_id"] = ObjectId(value["_id"])
        data = db_initialization.users_collection.find(value)
    data = db_initialization.users_collection.find(value)
    return list(data)


# insert a user
@user_app.post("/insert")
def insert_user(info: User):
    data = info.dict()
    if data["watched_movies"]:
        for movie in data["watched_movies"]:
            movie_data = db_initialization.movies_collection.find({"_id": ObjectId(movie)})
            if not movie_data:
                return f"movie doesnt exist{movie}"
        for movie in data["watched_movies"]:
            find_average(movie, data["rating"][movie], function="add")

        result = db_initialization.users_collection.insert_one(data)
        if result:
            get_data = list(db_initialization.users_collection.find({"_id": result.inserted_id}))
            return {"new user inserted": get_data}
        else:
            return "Insertion failed"
    else:
        raise HTTPException(status_code=404, detail="movie not found")


@user_app.put("/")
def update_user(movie_id: str, user_id: str, rating: int):
    result = list(
        db_initialization.users_collection.find({"_id": ObjectId(user_id)}, {"_id": False, "watched_movies": True}))
    if ObjectId(movie_id) in result[0]["watched_movies"]:
        raise HTTPException(status_code=404, detail="movie already exist ")
    else:
        final_value = find_average(movie_id, rating, function="add")
        s = update_details(movie_id, user_id, rating)
        return "successfully updated"



@user_app.delete("/")
def delete_user(ids: list):
    if ids:
        for i in ids:
            data = list(db_initialization.users_collection.find({"_id": ObjectId(i)}, {"_id": False, "rating": True}))
            d1 = data[0]["rating"]
            for movie, rating in d1.items():
                find_average(movie, rating, function="remove")
            db_initialization.users_collection.find_one_and_delete({"_id": ObjectId(i)})
        return f"sucessfully deleted{ids}"
    else:
        return "deletion failed"


@user_app.put("/insert filter")
def update_details(movie_id: str, user_id: str, rating: int):
    result = list(
        db_initialization.users_collection.find({"_id": ObjectId(user_id)},
                                                {"_id": False, "watched_movies": True, "rating": True}))
    print(result)
    result[0]["watched_movies"].append(ObjectId(movie_id))
    result[0]["rating"][movie_id] = rating
    query = {"_id": ObjectId(user_id)}
    update = {"$set": result[0]}
    data = db_initialization.users_collection.update_one(query, update)
    return "sucessfully updated movie"


def find_average(movie_id: str, new_rating: int, function: str):
    x = list(
        db_initialization.movies_collection.find({"_id": ObjectId(movie_id)}, {"_id": False, "overall_ratings": True}))
    rate = list(x[0]["overall_ratings"].keys())
    count = list(x[0]["overall_ratings"].values())

    if function == "remove":
        if count[0] > 1:
            new_avg = ((count[0] * float(rate[0])) - new_rating) / (count[0] - 1)
        if count[0] == 1:
            new_avg = 0
        if new_avg >= 60:
            query = {"$set": {"status": "hit", "overall_ratings": {str(new_avg): count[0] - 1}}}
            db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
            return "success"

        query = {"$set": {"status": "flop", "overall_ratings": {str(new_avg): count[0] - 1}}}
        db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
        return "success"

    if function == "add":
        new_avg = ((count[0] * float(rate[0])) + new_rating) / (count[0] + 1)
        if new_avg >= 60:
            query = {"$set": {"status": "hit", "overall_ratings": {str(new_avg): count[0] + 1}}}

            db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
            return "success"

        query = {"$set": {"status": "flop", "overall_ratings": {str(new_avg): count[0] + 1}}}
        db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
        return "success"
