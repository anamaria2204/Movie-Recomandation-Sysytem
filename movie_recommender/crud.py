import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class MovieRepository:
    """Handles movie, user, and rating CRUD operations with JSON persistence."""

    def __init__(self, storage_file: str = "data/movies_data.json"):
        self.storage_file = Path(storage_file)
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.movies: Dict[int, Dict[str, Any]] = {}
        self.users: Dict[int, Dict[str, Any]] = {}
        self.ratings: Dict[Tuple[int, int], int] = {}
        self._load_data()

    def _next_movie_id(self) -> int:
        return max(self.movies.keys(), default=0) + 1

    def _next_user_id(self) -> int:
        return max(self.users.keys(), default=0) + 1

    def _save_data(self) -> None:
        payload = {
            "movies": list(self.movies.values()),
            "users": list(self.users.values()),
            "ratings": [
                {"user_id": user_id, "movie_id": movie_id, "score": score}
                for (user_id, movie_id), score in self.ratings.items()
            ],
        }
        with self.storage_file.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

    def _load_data(self) -> None:
        if not self.storage_file.exists():
            return

        try:
            with self.storage_file.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except (json.JSONDecodeError, OSError):
            return

        self.movies = {int(movie["id"]): movie for movie in payload.get("movies", [])}
        self.users = {int(user["id"]): user for user in payload.get("users", [])}
        self.ratings = {
            (int(r["user_id"]), int(r["movie_id"])): int(r["score"])
            for r in payload.get("ratings", [])
        }

        for movie_id in self.movies:
            self._recalculate_movie_rating(movie_id)

    def _recalculate_movie_rating(self, movie_id: int) -> None:
        movie = self.movies.get(movie_id)
        if movie is None:
            return

        scores = [
            score for (user_id, rating_movie_id), score in self.ratings.items() if rating_movie_id == movie_id
        ]

        if not scores:
            movie["avg_rating"] = 0.0
            movie["review_count"] = 0
            return

        movie["avg_rating"] = round(sum(scores) / len(scores), 2)
        movie["review_count"] = len(scores)

    def _validate_movie_data(self, title: str, release_year: int, genres: List[str], director: str) -> None:
        if not title or not title.strip():
            raise ValueError("Movie title cannot be empty.")
        if not isinstance(release_year, int) or not (1888 <= release_year <= datetime.now().year + 2):
            raise ValueError("Release year must be a valid number between 1888 and next 2 years.")
        if not isinstance(genres, list):
            raise ValueError("Genres must be provided as a list.")
        if not director or not director.strip():
            raise ValueError("Director cannot be empty.")

    def add_movie(
        self,
        title: str,
        release_year: int,
        genres: Optional[List[str]] = None,
        director: str = "",
        **extra_fields: Any,
    ) -> Dict[str, Any]:
        normalized_genres = genres or []
        self._validate_movie_data(title, release_year, normalized_genres, director)

        movie_id = self._next_movie_id()
        movie = {
            "id": movie_id,
            "title": title.strip(),
            "release_year": release_year,
            "genres": [genre.strip() for genre in normalized_genres if genre and genre.strip()],
            "director": director.strip(),
            "avg_rating": 0.0,
            "review_count": 0,
        }
        movie.update(extra_fields)
        self.movies[movie_id] = movie
        self._save_data()
        return dict(movie)

    def get_movie(self, movie_id: int) -> Optional[Dict[str, Any]]:
        movie = self.movies.get(movie_id)
        if movie is None:
            return None
        return dict(movie)

    def get_all_movies(self) -> List[Dict[str, Any]]:
        return [dict(movie) for movie in sorted(self.movies.values(), key=lambda item: item["id"])]

    def update_movie(self, movie_id: int, **updates: Any) -> Optional[Dict[str, Any]]:
        movie = self.movies.get(movie_id)
        if movie is None:
            return None

        if "title" in updates:
            title = str(updates["title"]).strip()
            if not title:
                raise ValueError("Movie title cannot be empty.")
            movie["title"] = title

        if "release_year" in updates:
            year = int(updates["release_year"])
            if not (1888 <= year <= datetime.now().year + 2):
                raise ValueError("Release year must be valid.")
            movie["release_year"] = year

        if "genres" in updates:
            genres = updates["genres"]
            if not isinstance(genres, list):
                raise ValueError("Genres must be provided as a list.")
            movie["genres"] = [genre.strip() for genre in genres if genre and str(genre).strip()]

        if "director" in updates:
            director = str(updates["director"]).strip()
            if not director:
                raise ValueError("Director cannot be empty.")
            movie["director"] = director

        for key, value in updates.items():
            if key not in {"title", "release_year", "genres", "director"}:
                movie[key] = value

        self._save_data()
        return dict(movie)

    def delete_movie(self, movie_id: int) -> bool:
        if movie_id not in self.movies:
            return False

        del self.movies[movie_id]
        self.ratings = {
            (user_id, rating_movie_id): score
            for (user_id, rating_movie_id), score in self.ratings.items()
            if rating_movie_id != movie_id
        }
        self._save_data()
        return True

    def delete_all_movies(self) -> None:
        self.movies = {}
        self.ratings = {}
        self._save_data()

    def add_user(self, name: str) -> Dict[str, Any]:
        if not name or not str(name).strip():
            raise ValueError("User name cannot be empty.")

        user_id = self._next_user_id()
        user = {"id": user_id, "name": str(name).strip()}
        self.users[user_id] = user
        self._save_data()
        return dict(user)

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        user = self.users.get(user_id)
        if user is None:
            return None
        return dict(user)

    def get_all_users(self) -> List[Dict[str, Any]]:
        return [dict(user) for user in sorted(self.users.values(), key=lambda item: item["id"])]

    def update_user(self, user_id: int, **updates: Any) -> Optional[Dict[str, Any]]:
        user = self.users.get(user_id)
        if user is None:
            return None

        if "name" in updates:
            name = str(updates["name"]).strip()
            if not name:
                raise ValueError("User name cannot be empty.")
            user["name"] = name

        for key, value in updates.items():
            if key != "name":
                user[key] = value

        self._save_data()
        return dict(user)

    def delete_user(self, user_id: int) -> bool:
        if user_id not in self.users:
            return False

        del self.users[user_id]
        self.ratings = {
            (rating_user_id, movie_id): score
            for (rating_user_id, movie_id), score in self.ratings.items()
            if rating_user_id != user_id
        }
        self._save_data()
        return True

    def delete_all_users(self) -> None:
        self.users = {}
        self.ratings = {}
        self._save_data()

    def add_rating(self, user_id: int, movie_id: int, score: int) -> Dict[str, Any]:
        if user_id not in self.users:
            raise ValueError(f"User {user_id} does not exist.")
        if movie_id not in self.movies:
            raise ValueError(f"Movie {movie_id} does not exist.")
        if not isinstance(score, int) or not 1 <= score <= 5:
            raise ValueError("Movie rating must be an integer between 1 and 5.")

        self.ratings[(user_id, movie_id)] = score
        self._recalculate_movie_rating(movie_id)
        self._save_data()

        return {
            "user_id": user_id,
            "movie_id": movie_id,
            "score": score,
        }
