from dataclasses import dataclass, field
from typing import List


@dataclass
class Movie:
    id: int
    title: str
    release_year: int
    genres: List[str] = field(default_factory=list)
    director: str = ""
    avg_rating: float = 0.0
    review_count: int = 0


@dataclass
class User:
    id: int
    name: str


@dataclass
class Rating:
    user_id: int
    movie_id: int
    score: int
