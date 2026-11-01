import pytest

from movie_recommender.search_sort import (
    genre_report,
    most_active_users,
    search_movies,
    sort_movies,
    top_rated_movies,
)


def make_movie(id, title, year, genres, director, avg, count):
    return {
        "id": id,
        "title": title,
        "release_year": year,
        "genres": genres,
        "director": director,
        "avg_rating": avg,
        "review_count": count,
    }


@pytest.fixture
def movies():
    return [
        make_movie(1, "The Matrix", 1999, ["Sci-Fi", "Action"], "Wachowski", 4.5, 10),
        make_movie(2, "Matrix Reloaded", 2003, ["Sci-Fi", "Action"], "Wachowski", 3.5, 4),
        make_movie(3, "Amelie", 2001, ["Romance", "Comedy"], "Jeunet", 4.0, 2),
        make_movie(4, "Unrated", 1995, ["Drama"], "Nobody", 0.0, 0),
    ]


def test_search_partial_title(movies):
    assert [m["id"] for m in search_movies(movies, title="matrix")] == [1, 2]


def test_search_decade_and_director(movies):
    assert [m["id"] for m in search_movies(movies, decade=2000, director="jeun")] == [3]


def test_search_genres_any_vs_all(movies):
    assert len(search_movies(movies, genres=["Sci-Fi", "Comedy"])) == 3
    assert len(search_movies(movies, genres=["Sci-Fi", "Comedy"], match_all_genres=True)) == 0


def test_sort_by_rating_and_title(movies):
    assert [m["id"] for m in sort_movies(movies, "Highest rated")][:2] == [1, 3]
    assert sort_movies(movies, "Title (A-Z)")[0]["title"] == "Amelie"


def test_sort_unknown_sorter(movies):
    with pytest.raises(ValueError):
        sort_movies(movies, "nope")


def test_top_rated_respects_min_reviews(movies):
    assert [m["id"] for m in top_rated_movies(movies, n=5, min_reviews=3)] == [1, 2]


def test_genre_report(movies):
    report = {row["genre"]: row for row in genre_report(movies)}
    assert report["Sci-Fi"]["movie_count"] == 2
    assert report["Sci-Fi"]["avg_rating"] == 4.0
    assert report["Drama"]["avg_rating"] == 0.0


def test_most_active_users():
    users = [{"id": 1, "name": "Ana"}, {"id": 2, "name": "Bob"}]
    ratings = {(1, 1): 5, (1, 2): 4, (2, 1): 3}
    result = most_active_users(users, ratings, n=1)
    assert result == [{"user_id": 1, "name": "Ana", "review_count": 2}]
