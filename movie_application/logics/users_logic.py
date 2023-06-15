
from movie_application.database import db_initialization
from fastapi import APIRouter, HTTPException, Query
import pydantic
from typing import Dict, Optional

from bson.objectid import ObjectId
from movie_application.models.users_model import User

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

user_app = APIRouter()


# search a user

@user_app.post('/user/search')
def read_user(value: Dict):
    if "_id" in value.keys():
        value["_id"] = ObjectId(value["_id"])
    data = db_initialization.users_collection.find(value)
    return list(data)


# insert a user
@user_app.post("/user/insert")
def insert_user(info: User):
    data = info.dict()
    if data["watched_movies"]:
        for movie in data["watched_movies"]:
            movie_data = db_initialization.movies_collection.find({"_id": ObjectId(movie)})
            if not movie_data:
                return f"movie doesnt exist{movie}"
        for movie in data["watched_movies"]:
            if movie in data["rating"].keys():
                status = find_average(movie, data["rating"][movie], function="add")
                if status == False:
                    return "Failed to update the movie rating with the provided ratings "

        result = db_initialization.users_collection.insert_one(data)
        if result:
            get_data = list(db_initialization.users_collection.find({"_id": result.inserted_id}))
            return {"new user inserted": get_data}
        else:
            return "Insertion failed"
    else:
        raise HTTPException(status_code=404, detail="movie not found")


@user_app.put("/user/update")
def update_user(user_id: str, value: Dict):
    if value.get("_id"):
        return "Cannot update unique Object Id"
    if value.get("rating"):
        return "Ratings cannot be updated remove ratings and try again"
    query = {"_id": ObjectId(user_id)}
    update = {"$set": value}
    data = db_initialization.users_collection.find_one_and_update(query, update, return_document=True)
    if data:
        return data
    else:
        return "updating failed"


@user_app.delete("/user/delete")
def delete_user(ids: list):
    if ids:
        for i in ids:
            data = list(db_initialization.users_collection.find({"_id": ObjectId(i)}, {"_id": False, "rating": True}))
            d1 = data[0]["rating"]
            for movie, rating in d1.items():
                find_average(movie, rating, function="remove")
            db_initialization.users_collection.find_one_and_delete({"_id": ObjectId(i)})
        return "successfully deleted"
    else:
        return "deletion failed"


@user_app.put("/user/watch_movie")
def add_movie( rating: Optional[int]=None,movie_id:str=Query(...), user_id:str=Query(...)):
    result = list(
        db_initialization.users_collection.find({"_id": ObjectId(user_id)},
                                                {"_id": False, "watched_movies": True, "rating": True}))
    if result:
        if movie_id in result[0]["watched_movies"]:
            return "Already watched this movie"
        result[0]["watched_movies"].append(ObjectId(movie_id))
        if rating:
            if movie_id in  result[0]["rating"].keys():
                return f"Already rated the movie {movie_id}"
            result[0]["rating"][movie_id] = rating
            status = find_average(movie_id, rating, function="add")
            if not status:
                return "Failed to update the movie rating with the provided ratings "

    query = {"_id": ObjectId(user_id)}
    update = {"$set": result[0]}
    data = db_initialization.users_collection.find_one_and_update(query, update,return_document=True)
    return f"sucessfully added movie - {data}"


def find_average(movie_id: str, new_rating: int, function: str):
    x = list(
        db_initialization.movies_collection.find({"_id": ObjectId(movie_id)}))
    if not x:
        return False
    rate = x[0]['overall_ratings']
    count = x[0]['number_of_ratings']

    if function == "remove":
        new_avg = 0
        if count > 1:
            new_avg = ((count * float(rate)) - new_rating) / (count - 1)
        if count == 1:
            new_avg = 0
        if new_avg >= 60:
            query = {"$set": {"status": "hit", "overall_ratings": new_avg, "number_of_ratings":count - 1}}
            db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
            return "success"

        query = {"$set": {"status": "flop", "overall_ratings": new_avg, "number_of_ratings":count - 1}}
        db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
        return "success"

    if function == "add":
        new_avg = ((count * float(rate)) + new_rating) / (count + 1)
        if new_avg >= 60:
            query = {"$set": {"status": "hit", "overall_ratings": new_avg, "number_of_ratings": count + 1}}

            db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
            return "success"

        query = {"$set": {"status": "hit", "overall_ratings": new_avg, "number_of_ratings": count + 1}}
        db_initialization.movies_collection.update_one({"_id": ObjectId(movie_id)}, query)
        return "success"
