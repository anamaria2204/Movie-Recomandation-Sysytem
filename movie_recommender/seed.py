from movie_recommender.crud import MovieRepository

# (title, release_year, genres, director)
SAMPLE_MOVIES = [
    ("The Shawshank Redemption", 1994, ["Drama"], "Frank Darabont"),
    ("The Godfather", 1972, ["Crime", "Drama"], "Francis Ford Coppola"),
    ("The Dark Knight", 2008, ["Action", "Crime", "Drama"], "Christopher Nolan"),
    ("Pulp Fiction", 1994, ["Crime", "Drama"], "Quentin Tarantino"),
    ("Forrest Gump", 1994, ["Drama", "Romance"], "Robert Zemeckis"),
    ("Inception", 2010, ["Action", "Sci-Fi", "Thriller"], "Christopher Nolan"),
    ("The Matrix", 1999, ["Action", "Sci-Fi"], "Lana Wachowski"),
    ("Interstellar", 2014, ["Adventure", "Drama", "Sci-Fi"], "Christopher Nolan"),
    ("Fight Club", 1999, ["Drama", "Thriller"], "David Fincher"),
    ("Goodfellas", 1990, ["Crime", "Drama"], "Martin Scorsese"),
    ("Parasite", 2019, ["Comedy", "Drama", "Thriller"], "Bong Joon-ho"),
    ("Spirited Away", 2001, ["Animation", "Adventure", "Fantasy"], "Hayao Miyazaki"),
    ("Toy Story", 1995, ["Animation", "Comedy", "Adventure"], "John Lasseter"),
    ("The Lion King", 1994, ["Animation", "Adventure", "Drama"], "Roger Allers"),
    ("Amelie", 2001, ["Comedy", "Romance"], "Jean-Pierre Jeunet"),
    ("Gladiator", 2000, ["Action", "Adventure", "Drama"], "Ridley Scott"),
    ("Titanic", 1997, ["Drama", "Romance"], "James Cameron"),
    ("Jurassic Park", 1993, ["Adventure", "Sci-Fi", "Thriller"], "Steven Spielberg"),
    ("La La Land", 2016, ["Comedy", "Drama", "Romance"], "Damien Chazelle"),
    ("Mad Max: Fury Road", 2015, ["Action", "Adventure", "Sci-Fi"], "George Miller"),
]

SAMPLE_USERS = ["Alice", "Bob", "Carla", "David", "Elena"]

# (user index, movie index, score) — indexes into the lists above, 0-based
SAMPLE_RATINGS = [
    (0, 0, 5), (0, 1, 5), (0, 2, 4), (0, 5, 4), (0, 10, 5), (0, 14, 4),
    (1, 2, 5), (1, 5, 5), (1, 6, 4), (1, 7, 5), (1, 17, 4), (1, 19, 4),
    (2, 4, 4), (2, 14, 5), (2, 16, 4), (2, 18, 5), (2, 11, 5), (2, 12, 4),
    (3, 1, 5), (3, 3, 5), (3, 8, 4), (3, 9, 5), (3, 0, 4), (3, 2, 5),
    (4, 11, 5), (4, 12, 5), (4, 13, 4), (4, 7, 4), (4, 10, 4), (4, 6, 3),
]


def load_sample_data(repo: MovieRepository) -> None:
    """Add sample movies, users and ratings to the repository."""
    movies = [
        repo.add_movie(title=t, release_year=y, genres=g, director=d)
        for t, y, g, d in SAMPLE_MOVIES
    ]
    users = [repo.add_user(name) for name in SAMPLE_USERS]
    for user_idx, movie_idx, score in SAMPLE_RATINGS:
        repo.add_rating(users[user_idx]["id"], movies[movie_idx]["id"], score)
