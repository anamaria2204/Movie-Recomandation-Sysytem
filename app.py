import pandas as pd
import streamlit as st

from movie_recommender.crud import MovieRepository
from movie_recommender.seed import load_sample_data
from movie_recommender.search_sort import (
    SORTERS,
    all_decades,
    all_genres,
    genre_report,
    most_active_users,
    search_movies,
    sort_movies,
    top_rated_movies,
)

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")


@st.cache_resource
def get_repo() -> MovieRepository:
    # Streamlit reruns this whole script on every click; cache_resource keeps
    # one repository object alive across reruns instead of reloading the JSON.
    repo = MovieRepository(storage_file="data/movies_data.json")
    # Fresh start (e.g. first run on Streamlit Cloud): fill with sample data.
    if not repo.movies and not repo.users:
        load_sample_data(repo)
    return repo


repo = get_repo()


def movies_table(movies):
    df = pd.DataFrame(movies)
    if df.empty:
        return df
    df["genres"] = df["genres"].apply(", ".join)
    columns = ["id", "title", "release_year", "genres", "director", "avg_rating", "review_count"]
    return df[columns]


def user_options():
    return {f"{u['id']} - {u['name']}": u["id"] for u in repo.get_all_users()}


def movie_options():
    return {f"{m['id']} - {m['title']} ({m['release_year']})": m["id"] for m in repo.get_all_movies()}


# ---------- Pages ----------

def page_movies():
    st.header("Movies")
    tab_list, tab_add, tab_edit = st.tabs(["Catalog", "Add", "Edit / Delete"])

    with tab_list:
        movies = repo.get_all_movies()
        if movies:
            st.dataframe(movies_table(movies), hide_index=True, use_container_width=True)
        else:
            st.info("No movies yet. Add one in the 'Add' tab.")

    with tab_add:
        with st.form("add_movie", clear_on_submit=True):
            title = st.text_input("Title")
            year = st.number_input("Release year", min_value=1888, max_value=2100, value=2000, step=1)
            genres = st.text_input("Genres (comma separated)")
            director = st.text_input("Director")
            if st.form_submit_button("Add movie"):
                try:
                    movie = repo.add_movie(
                        title=title,
                        release_year=int(year),
                        genres=[g.strip() for g in genres.split(",") if g.strip()],
                        director=director,
                    )
                    st.success(f"Added '{movie['title']}' (id {movie['id']}).")
                except ValueError as error:
                    st.error(str(error))

    with tab_edit:
        options = movie_options()
        if not options:
            st.info("No movies to edit.")
            return
        label = st.selectbox("Movie", list(options))
        movie = repo.get_movie(options[label])
        with st.form(f"edit_movie_{movie['id']}"):
            title = st.text_input("Title", value=movie["title"])
            year = st.number_input("Release year", min_value=1888, max_value=2100, value=movie["release_year"])
            genres = st.text_input("Genres (comma separated)", value=", ".join(movie["genres"]))
            director = st.text_input("Director", value=movie["director"])
            if st.form_submit_button("Save changes"):
                try:
                    repo.update_movie(
                        movie["id"],
                        title=title,
                        release_year=int(year),
                        genres=[g.strip() for g in genres.split(",") if g.strip()],
                        director=director,
                    )
                    st.success("Movie updated.")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
        if st.button("Delete this movie", type="primary"):
            repo.delete_movie(movie["id"])
            st.rerun()


def page_users():
    st.header("Users & Ratings")
    col_users, col_rate = st.columns(2)

    with col_users:
        st.subheader("Users")
        with st.form("add_user", clear_on_submit=True):
            name = st.text_input("New user name")
            if st.form_submit_button("Add user"):
                try:
                    user = repo.add_user(name)
                    st.success(f"Added user {user['name']} (id {user['id']}).")
                except ValueError as error:
                    st.error(str(error))

        users = repo.get_all_users()
        if users:
            st.dataframe(pd.DataFrame(users), hide_index=True, use_container_width=True)
            options = user_options()
            label = st.selectbox("Select user to delete", list(options))
            if st.button("Delete user"):
                repo.delete_user(options[label])
                st.rerun()
        else:
            st.info("No users yet.")

    with col_rate:
        st.subheader("Rate a movie")
        users, movies = user_options(), movie_options()
        if not users or not movies:
            st.info("You need at least one user and one movie to add a rating.")
            return
        with st.form("add_rating"):
            user_label = st.selectbox("User", list(users))
            movie_label = st.selectbox("Movie", list(movies))
            score = st.slider("Score", 1, 5, 3)
            if st.form_submit_button("Submit rating"):
                try:
                    repo.add_rating(users[user_label], movies[movie_label], score)
                    st.success("Rating saved. Average updated.")
                except ValueError as error:
                    st.error(str(error))


def page_search():
    st.header("Search & Sort")
    movies = repo.get_all_movies()
    if not movies:
        st.info("No movies yet.")
        return

    col1, col2, col3 = st.columns(3)
    title = col1.text_input("Title contains")
    director = col2.text_input("Director contains")
    decade = col3.selectbox("Decade", [None] + all_decades(movies), format_func=lambda d: "Any" if d is None else f"{d}s")

    col4, col5, col6, col7 = st.columns([3, 1, 2, 1])
    genres = col4.multiselect("Genres", all_genres(movies))
    match_all = col5.checkbox("Match all genres")
    sorter = col6.selectbox("Sort by", list(SORTERS))
    flip = col7.checkbox("Reverse order")

    results = search_movies(movies, title=title, director=director, genres=genres, match_all_genres=match_all, decade=decade)
    natural = sort_movies(results, sorter)
    results = natural[::-1] if flip else natural

    st.caption(f"{len(results)} of {len(movies)} movies")
    if results:
        st.dataframe(movies_table(results), hide_index=True, use_container_width=True)


def page_reports():
    st.header("Reports")
    movies = repo.get_all_movies()
    if not movies:
        st.info("No movies yet.")
        return

    st.subheader("Top rated movies")
    col1, col2 = st.columns(2)
    n = col1.number_input("Top N", min_value=1, value=5)
    min_reviews = col2.number_input("Minimum reviews (M)", min_value=1, value=1)
    top = top_rated_movies(movies, n=int(n), min_reviews=int(min_reviews))
    if top:
        st.dataframe(movies_table(top), hide_index=True, use_container_width=True)
    else:
        st.info("No movie has that many reviews yet.")

    st.subheader("Genre breakdown")
    report = genre_report(movies)
    if report:
        df = pd.DataFrame(report)
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.bar_chart(df.set_index("genre")["movie_count"])

    st.subheader("Most active users")
    active = most_active_users(repo.get_all_users(), repo.ratings, n=10)
    if active:
        st.dataframe(pd.DataFrame(active), hide_index=True, use_container_width=True)
    else:
        st.info("No users yet.")


PAGES = {
    "Movies": page_movies,
    "Users & Ratings": page_users,
    "Search & Sort": page_search,
    "Reports": page_reports,
}

st.sidebar.title("🎬 Movie Recommender")
PAGES[st.sidebar.radio("Go to", list(PAGES))]()
