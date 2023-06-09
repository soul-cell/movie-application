from fastapi import FastAPI
from movie_application.logics.movie_logic import new_app


app = FastAPI()


app.include_router(new_app, tags=["movie"], prefix="/movie")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)