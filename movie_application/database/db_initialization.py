import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["Movie_app"]
movies_collection = mydb["movie"]
users_collection = mydb["users"]