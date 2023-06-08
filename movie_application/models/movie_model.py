from pydantic import BaseModel, Field
from enum import Enum


class overallstatus(str, Enum):
    HIT = "hit"
    FLOP = "flop"


class movie(BaseModel):
    moviename: str = Field(...)
    director: str = Field(...)
    producer: str = Field(...)
    cast: dict = Field(...)
    subtitles: list = Field(...)
    languages: list = Field(...)
    genres: list = Field(...)
    status: overallstatus
    release_date: str = Field(...)
    revenue_collections: int = Field(...)
    overall_ratings: int = Field(...)





