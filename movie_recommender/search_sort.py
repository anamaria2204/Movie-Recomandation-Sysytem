from typing import Any, Callable, Dict, List, Optional, Tuple

Movie = Dict[str, Any]

# Sorters are plain lambdas stored in a dict, so the UI can list them by name.
SORTERS: Dict[str, Callable[[Movie], Any]] = {
    "Highest rated": lambda m: (m["avg_rating"], m["review_count"]),
    "Most reviewed": lambda m: (m["review_count"], m["avg_rating"]),
    "Newest": lambda m: m["release_year"],
    "Title (A-Z)": lambda m: m["title"].lower(),
}

# Sorters whose natural order is ascending (everything else is descending).
ASCENDING_SORTERS = {"Title (A-Z)"}


def search_movies(
    movies: List[Movie],
    title: str = "",
    director: str = "",
    genres: Optional[List[str]] = None,
    match_all_genres: bool = False,
    decade: Optional[int] = None,
) -> List[Movie]:
    """Filter movies by partial title/director, genre set, and release decade (e.g. 1990)."""
    title = title.strip().lower()
    director = director.strip().lower()
    wanted = {g.lower() for g in (genres or [])}

    results = []
    for movie in movies:
        if title and title not in movie["title"].lower():
            continue
        if director and director not in movie["director"].lower():
            continue
        if decade is not None and movie["release_year"] // 10 * 10 != decade:
            continue
        if wanted:
            movie_genres = {g.lower() for g in movie["genres"]}
            matches = wanted <= movie_genres if match_all_genres else bool(wanted & movie_genres)
            if not matches:
                continue
        results.append(movie)
    return results


def sort_movies(movies: List[Movie], sorter: str, descending: Optional[bool] = None) -> List[Movie]:
    """Sort with one of the named SORTERS. Direction defaults to the sorter's natural order."""
    if sorter not in SORTERS:
        raise ValueError(f"Unknown sorter '{sorter}'. Choose from: {', '.join(SORTERS)}")
    if descending is None:
        descending = sorter not in ASCENDING_SORTERS
    return sorted(movies, key=SORTERS[sorter], reverse=descending)


def all_genres(movies: List[Movie]) -> List[str]:
    return sorted({g for m in movies for g in m["genres"]})


def all_decades(movies: List[Movie]) -> List[int]:
    return sorted({m["release_year"] // 10 * 10 for m in movies})


def top_rated_movies(movies: List[Movie], n: int = 5, min_reviews: int = 1) -> List[Movie]:
    """Top N movies by average rating among those with at least min_reviews reviews."""
    eligible = [m for m in movies if m["review_count"] >= min_reviews]
    return sort_movies(eligible, "Highest rated")[:n]


def genre_report(movies: List[Movie]) -> List[Dict[str, Any]]:
    """Movie count and average rating (of rated movies) per genre."""
    stats: Dict[str, Dict[str, Any]] = {}
    for movie in movies:
        for genre in movie["genres"]:
            entry = stats.setdefault(genre, {"genre": genre, "movie_count": 0, "ratings": []})
            entry["movie_count"] += 1
            if movie["review_count"] > 0:
                entry["ratings"].append(movie["avg_rating"])

    report = []
    for entry in stats.values():
        ratings = entry["ratings"]
        report.append(
            {
                "genre": entry["genre"],
                "movie_count": entry["movie_count"],
                "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else 0.0,
            }
        )
    return sorted(report, key=lambda row: (-row["movie_count"], row["genre"]))


def most_active_users(
    users: List[Dict[str, Any]], ratings: Dict[Tuple[int, int], int], n: int = 5
) -> List[Dict[str, Any]]:
    """Users ranked by number of ratings given."""
    counts: Dict[int, int] = {}
    for user_id, _movie_id in ratings:
        counts[user_id] = counts.get(user_id, 0) + 1

    report = [
        {"user_id": u["id"], "name": u["name"], "review_count": counts.get(u["id"], 0)}
        for u in users
    ]
    return sorted(report, key=lambda row: (-row["review_count"], row["name"]))[:n]
