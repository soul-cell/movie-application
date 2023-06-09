import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["Movie_app"]
collection_list = mydb.list_collection_names()
for collection in collection_list:
    mydb.drop_collection(collection)
movies_collection = mydb["movie"]
users_collection = mydb["users"]
movies_doc = [{

    "movie_name": "Avengers-Endgame",
    "director": "Anthony Russo",
    "producer": "Joe Russo",
    "cast": {"actor": "Robert Downey Jr.", "villian": "Thanos", "supporting roles": "Chris Hemsworth"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "kannadam", "chinese"],
    "languages": ["english", "tamil", "malayalam", "hindi"],
    "genres": ["action", "romance"],
    "status": "hit",
    "release_date": "26/04/2019",
    "revenue_collections": 26517181,
    "overall_ratings": 84
}, {
    "movie_name": "Inception",
    "director": "Christopher Nolan",
    "producer": "Tom Berenger",
    "cast": {"actor": "Tom Hardy", "villian": "Leonardo DiCaprio", "supporting roles": "Elliot Page"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "kannadam", "chinese"],
    "languages": ["english", "tamil", "malayalam", "hindi"],
    "genres": ["action", "thriller"],
    "status": "flop",
    "release_date": "16/07/2010",
    "revenue_collections": 26517181,
    "overall_ratings": 49
}, {
    "movie_name": "Titanic",
    "director": "James Cameron",
    "producer": "Bill Paxton",
    "cast": {"actor": "Leonardo DiCaprio", "villian": "Jonathan Hyde", "supporting roles": "Billy Zane"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "kannadam", "chinese"],
    "languages": ["english", "tamil", "malayalam", "hindi"],
    "genres": ["romance", "action"],
    "status": "hit",
    "release_date": "20/12/1997",
    "revenue_collections": 26517181,
    "overall_ratings": 79

}, {

    "movie_name": "Avatar",
    "director": "James Cameron",
    "producer": "Stephen Lang",
    "cast": {"actor": "Sam Worthington", "villian": "Zoe Saldana", "supporting roles": "Sigourney Weaver"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "kannadam", "chinese"],
    "languages": ["english", "tamil", "malayalam", "hindi"],
    "genres": ["action", "romance"],
    "status": "hit",
    "release_date": "10/12/2009",
    "revenue_collections": 26517181,
    "overall_ratings": 78

}, {
    "movie_name": "Jungle Cruise,",
    "director": "Jaume Collet-Serra",
    "producer": "John Requa",
    "cast": {"actor": "Dwayne Douglas Johnson", "villian": "Paul Edward Valentine",
             "supporting roles": "James Newton Howard"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "kannadam", "chinese"],
    "languages": ["english", "tamil", "malayalam", "hindi"],
    "genres": ["adventure", "romance"],
    "status": "flop",
    "release_date": "24/07/2021",
    "revenue_collections": 1517101,
    "overall_ratings": 52
}]
users_doc = [{"name": "thiru", "age": 21, "watched_movies": ["Titanic", "Avengers endgame", "Avatar"],
            "rating": {"Titanic": 65, "Avengers endgame": 87, "Avatar": 75}},
             {"name": "yokesh", "age": 25, "watched_movies": ["Jungle Cruise", "Inception", "Avengers endgame"],
            "rating": {"Jungle Cruise": 43, "Inception": 89, "Avengers endgame": 76},
            }]

mv = users_collection.insert_many(users_doc)
res = movies_collection.insert_many(movies_doc)
print(res)
print(client.list_database_names())
print(mv)