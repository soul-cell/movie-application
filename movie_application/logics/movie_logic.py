
from movie_application.database import db_initialization
from fastapi import APIRouter, Query
from pydantic import json
from typing import Dict, Optional
from movie_application.models.movie_model import Movie
from bson.objectid import ObjectId

json.ENCODERS_BY_TYPE[ObjectId] = str

new_app = APIRouter()


@new_app.post('/movie/search')
def read_movie(values: Dict):
    if "_id" in values.keys():
        values["_id"] = ObjectId(values["_id"])
    data = list(db_initialization.movies_collection.find(values))
    return data


@new_app.post('/movie/insert')
def insert_movie(info: Movie):
    data = info.dict()
    result = db_initialization.movies_collection.insert_one(data)
    if result:
        data_get = read_movie({"_id": result.inserted_id})
        return data_get
    else:
        return "insertion failed"


@new_app.put("/movie/update")
def update_movie(movie_id: str, value: Dict):
    if value.get("_id"):
        return "Not possible to update the id"
    query = {"_id": ObjectId(movie_id)}
    update = {"$set": value}
    data = db_initialization.movies_collection.find_one_and_update(query, update, return_document=True)
    if data:
        return data
    else:
        return "updating failed"


@new_app.delete("/movie/delete")
def delete_movie(ids: list):
    non_deleted = []
    id_list = []
    for i in ids:
        result = db_initialization.movies_collection.find_one_and_delete({"_id": ObjectId(i)})
        if result:
            id_list.append(i)
        else:
            non_deleted.append(i)
    if non_deleted:
        return "non deleted ids:", non_deleted, "deleted ids:", id_list

    else:
        return f"successfully deleted and deleted ids are{id_list}"


@new_app.post('/movie/filter')
def filter_movies(
        category: Optional[list] = Query(None),
        ratings: str = None,
        director: str = None,
        producer: str = None,
        release_date: str = None,
        language: Optional[list] = Query(None),
        subtitles: Optional[list] = Query(None)
):
    query = {}
    if category:
        query1 = {"genres": {"$in": category}}
        query.update(query1)
    if ratings:
        ratings = float(ratings)
        query2 = {"overall_ratings": {"$gt": ratings}}
        query.update(query2)
    if director:
        query3 = {"director": director}
        query.update(query3)
    if producer:
        query4 = {"producer": producer}
        query.update(query4)
    if release_date:
        query5 = {"release_date": release_date}
        query.update(query5)
    if language:
        query6 = {"languages": {"$in": language}}
        query.update(query6)
    if subtitles:
        query7 = {"subtitles": {"$in": subtitles}}
        query.update(query7)
    data = read_movie(query)
    return data


@new_app.post('/movie/Sorted_ratings')
def sort_movie(sorting_order: str):
    sorting_order = sorting_order.lower()

    if sorting_order == "ascending":
        data = list(db_initialization.movies_collection.find().sort("overall_ratings", 1))
        return data

    if sorting_order == "descending":
        data = list(db_initialization.movies_collection.find().sort("overall_ratings", -1))
        return data
    else:
        return "Provide valid sorting order ascending/descending"
