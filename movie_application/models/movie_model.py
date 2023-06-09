from pydantic import BaseModel, Field
from enum import Enum


class OverallStatus(str, Enum):
    HIT = "hit"
    FLOP = "flop"


class Movie(BaseModel):
    moviename: str = Field(...)
    director: str = Field(...)
    producer: str = Field(...)
    cast: dict = Field(...)
    subtitles: list = Field(...)
    languages: list = Field(...)
    genres: list = Field(...)
    status: OverallStatus
    release_date: str = Field(...)
    revenue_collections: int = Field(...)
    overall_ratings: int = Field(...)





