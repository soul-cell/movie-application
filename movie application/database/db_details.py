import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Movie_app"]
mycollection = mydb["movie"]
users = mydb["users"]
myDoc = [{

    "movie_name": "gentle man",
    "director": "shankar",
    "producer": "deva",
    "cast": {"actor": "arjun", "villian": "b", "supporting roles": "c"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "chinese"],
    "languages": ["english", "tamil", "malayalam", "hindi"],
    "genres": ["horror", "romance"],
    "status": "hit",
    "release date": "2/12/2012",
    "revenue collections": 467547682,
    "overall ratings":78
}, {

    "movie_name": "don",
    "director": "mn",
    "producer": "s",
    "cast": {"actor": "shiva", "villian": "jdj", "supporting roles": "shivangi"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "kannadam"],
    "languages": ["tamil", "malayalam", "hindi"],
    "genres": ["action", "romance"],
    "status":  "flop",
    "release date": "7/12/2021",
    "revenue collections": 7353819,
    "overall ratings":54
}, {

    "movie_name": "nanban",
    "director": "fef",
    "producer": "gd",
    "cast": {"actor": "vijay", "villian": "fjc", "supporting roles": "jeeva"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "kannadam", "chinese"],
    "languages":["english", "tamil", "malayalam", "hindi"],
    "genres": ["comedy", "romance"],
    "status": "hit",
    "release date": "2/2/2022",
    "revenue collections": 4675476856,
    "overall ratings":86
}, {

    "movie_name": "three",
    "director": "atlee",
    "producer": "",
    "cast": {"actor": "eke", "villian": "fjsw", "supporting roles": "eaw"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "telugu", "kannadam", "chinese"],
    "languages": ["english", "tamil", "malayalam", "hindi"],
    "genres": ["action", "romance"],
    "status": "hit",
    "release date": "2/12/2012",
    "revenue collections": 26517181,
    "overall ratings":75

}, {

    "movie_name": "wf",
    "director": "d",
    "producer": "edkv",
    "cast": {"actor": "swkja", "villian": "mdk", "supporting roles": "djw"},
    "subtitles": ["english", "tamil", "malayalam", "hindi", "chinese"],
    "languages": ["english", "tamil", "malayalam", "hindi"],
    "genres": ["comedy", "romance"],
    "status":"flop",
    "release date": "19/7/2023",
    "revenue collections": 67547682,
    "overall ratings":53
}]
myusers = [{"name": "thiru", "age": 21, "watched movies": ["three", "nanban", "don"],
            "rating": {"three": 65, "nanban": 87, "don": 35}},
           {"name": "yokesh", "age": 25, "watched movies": ["wf", "gentleman", "don"],
            "rating": {"wf": 43, "gentleman": 89, "don": 46},
          }]

mv = users.insert_many(myusers)
res = mycollection.insert_many(myDoc)
print(res)
print(myclient.list_database_names())
print(mv)