from fastapi import FastAPI
from movie_application.logics.movie_logic import new_app
from movie_application.logics.users_logic import user_app

app = FastAPI()

app.include_router(new_app, tags=["movie"], prefix="/movie_app")

app.include_router(user_app, tags=["users"], prefix="/movie_app")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
