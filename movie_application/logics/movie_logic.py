from movie_application.database import db_details
from fastapi import APIRouter
import pydantic

from bson.objectid import ObjectId

pydantic.json.ENCODERS_BY_TYPE[ObjectId]= str

new_app = APIRouter()


@new_app.get('/mydoc')
def get_all_movie():
    data = db_details.mycollection.find()
    return list(data)

