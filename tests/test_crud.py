from movie_recommender.crud import MovieRepository


def test_add_and_get_movie():
    repo = MovieRepository(storage_file="test_movies.json")
    repo.delete_all_movies()

    movie = repo.add_movie(
        title="Inception",
        release_year=2010,
        genres=["Sci-Fi", "Thriller"],
        director="Christopher Nolan",
    )

    assert movie["id"] == 1
    assert repo.get_movie(1)["title"] == "Inception"


def test_update_and_delete_movie():
    repo = MovieRepository(storage_file="test_movies.json")
    repo.delete_all_movies()

    repo.add_movie(title="Dune", release_year=2021, genres=["Sci-Fi"], director="Denis Villeneuve")
    repo.update_movie(1, title="Dune Part Two", director="Denis Villeneuve")

    assert repo.get_movie(1)["title"] == "Dune Part Two"

    repo.delete_movie(1)
    assert repo.get_movie(1) is None


def test_add_user_and_rating():
    repo = MovieRepository(storage_file="test_movies.json")
    repo.delete_all_movies()
    repo.delete_all_users()

    repo.add_user(name="Alice")
    repo.add_movie(title="Interstellar", release_year=2014, genres=["Sci-Fi", "Drama"], director="Christopher Nolan")

    rating = repo.add_rating(user_id=1, movie_id=1, score=5)
    assert rating["score"] == 5
    assert repo.get_movie(1)["avg_rating"] == 5.0


def test_invalid_rating_is_rejected():
    repo = MovieRepository(storage_file="test_movies.json")
    repo.delete_all_movies()
    repo.delete_all_users()

    repo.add_user(name="Bob")
    repo.add_movie(title="Memento", release_year=2000, genres=["Mystery"], director="Christopher Nolan")

    try:
        repo.add_rating(user_id=1, movie_id=1, score=8)
        assert False, "Expected ValueError for invalid rating"
    except ValueError:
        pass
