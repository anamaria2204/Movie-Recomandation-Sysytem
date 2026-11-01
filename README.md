# Movie Recommender System

This project is a movie recommender system built with Python. The current version focuses on the core data management layer: movie and user CRUD operations, rating handling, and JSON persistence.

## Project s

Completed so far:
- Project structure created
- Movie repository implemented
- User management implemented
- Movie ratings added with validation
- Average rating logic added
- Data stored in JSON files
- Unit tests written and passing
- Simple interactive CLI created

This matches the first academic milestone from the course: basic CRUD and data management before moving to search, sorting, reports, and recommendation logic.

## Main features implemented

### 1. Movie management
The system lets you:
- add a movie
- view all movies
- update movie information
- delete a movie

Movie fields include:
- id
- title
- release_year
- genres
- director
- avg_rating
- review_count

### 2. User management
The system lets you:
- add a user
- view all users
- update a user
- delete a user

Each user has:
- id
- name

### 3. Ratings and validation
Users can rate movies from 1 to 5.
The system validates:
- invalid rating values
- missing user data
- missing movie data
- empty movie title
- empty director name
- invalid release year

When a rating is added, the movie average rating is recalculated automatically.

### 4. Data persistence
The repository stores data in JSON format so records remain saved between program runs.

## Project structure

```text
movie_recommender/
├── __init__.py
├── crud.py
├── models.py
├──

tests/
├── test_crud.py

main.py
README.md
requirements.txt
```

## How the app works

The project uses a central repository class called `MovieRepository`.

This class is responsible for:
- storing movies in memory
- storing users in memory
- storing ratings in memory
- saving all data to a JSON file
- retrieving records
- updating or deleting records
- recalculating movie averages

## Example workflow

A typical use flow is:
1. Add a user
2. Add a movie
3. Add a rating for that movie
4. View the movie list
5. Check the updated average rating

## Run the project

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the interactive app

```bash
python main.py
```

### Start the Streamlit app

```bash
streamlit run app.py
```

### Run tests

```bash
python -m pytest -q
```

### Iteration 2: Search, sorting, and reports
Planned features:
- search by title, genre, director, or year
- sort movies by rating, year, or popularity
- generate summary reports
- show top-rated movies
- show most active users

### Iteration 3: Recommendation engine
Planned features:
- content-based recommendation
- collaborative filtering
- user similarity logic
- recommendation suggestions based on tastes

### Advanced version
Later improvements may include:
- Pandas data analysis
- graphs and visual statistics
- GUI with Streamlit
- real dataset integration such as MovieLens

