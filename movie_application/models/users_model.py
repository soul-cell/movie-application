from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(...)
    age: int = Field(...)
    watched_movies: list = Field(...)
    rating: dict = Field(...)