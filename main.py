from movie_recommender.crud import MovieRepository


def print_menu():
    print("\nMovie Recommender System - CRUD Menu")
    print("1. Add movie")
    print("2. List movies")
    print("3. Update movie")
    print("4. Delete movie")
    print("5. Add user")
    print("6. List users")
    print("7. Add rating")
    print("8. Exit")


def main():
    repo = MovieRepository(storage_file="data/movies_data.json")

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            title = input("Title: ")
            year = int(input("Release year: "))
            genres = input("Genres (comma separated): ")
            director = input("Director: ")
            movie = repo.add_movie(
                title=title,
                release_year=year,
                genres=[g.strip() for g in genres.split(",") if g.strip()],
                director=director,
            )
            print("Movie added:", movie)

        elif choice == "2":
            movies = repo.get_all_movies()
            if not movies:
                print("No movies in the catalog.")
            else:
                for movie in movies:
                    print(movie)

        elif choice == "3":
            movie_id = int(input("Movie ID to update: "))
            title = input("New title (leave blank to keep): ")
            year = input("New release year (leave blank to keep): ")
            director = input("New director (leave blank to keep): ")
            updates = {}
            if title:
                updates["title"] = title
            if year:
                updates["release_year"] = int(year)
            if director:
                updates["director"] = director
            print(repo.update_movie(movie_id, **updates))

        elif choice == "4":
            movie_id = int(input("Movie ID to delete: "))
            print("Deleted successfully:", repo.delete_movie(movie_id))

        elif choice == "5":
            name = input("User name: ")
            print("User added:", repo.add_user(name))

        elif choice == "6":
            users = repo.get_all_users()
            if not users:
                print("No users registered.")
            else:
                for user in users:
                    print(user)

        elif choice == "7":
            user_id = int(input("User ID: "))
            movie_id = int(input("Movie ID: "))
            score = int(input("Rating (1-5): "))
            print(repo.add_rating(user_id=user_id, movie_id=movie_id, score=score))

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
