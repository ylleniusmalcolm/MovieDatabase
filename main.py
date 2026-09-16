from movie import Movie
from movie_registry import MovieRegistry
from review import Review

def print_movies(movies):
    print("--------------")
    for index, movie in enumerate(movies):
        print(f"{index + 1}: ", end="")
        movie.print_short()
        print("--------------")

def print_reviews(reviews):
    print("--------------")
    for review in reviews:
        review.print_review()
        print("--------------")

def leave_review_menu(movie):
    name = input("What's your name?\n")
    rating = 0
    while True:
        rating_input = input("Rate this movie 1-10: ")
        if not rating_input.isdigit() or int(rating_input) < 1 or int(rating_input) > 10:
            print("Invalid input")
            continue
        rating = int(rating_input)
        break

    review = Review(name, rating, movie.movie_uuid)
    review.generate_uuid()
    
    while True:
        print("Do you want to leave a written review?")
        print("1. Yes")
        print("2. No")
        selection = input("Please select and option: ")
        if not selection.isdigit():
            print("Invalid input")
            continue

        match int(selection):
            case 1:
                review.review_text = input("Text: ")
                break
            case 2:
                break
            
        print("Invalid input")
    
    registry.add_review(review)
        

def movie_options_menu(movie):
    while True:
        movie.print_long()
        print("--------------")
        print("Options:")
        print("1. Leave a review")
        print("2. Read reviews")
        print("0. Return to main menu")

        selection = input("Please select and option: ")
        if not selection.isdigit():
            print("Invalid input")
            continue

        match int(selection):
            case 1:
                leave_review_menu(movie)
                break
            case 2:
                print_reviews(registry.get_reviews(movie.movie_uuid))
                continue
            case 0:
                print("Returning to main menu")
                return
            
        print("Invalid input")

def select_movie_menu(movies):
    while True:
        print_movies(movies)
        selection = input("Select a movie (or 0 to return to main menu):")
        if not selection.isdigit():
            print("Invalid input")
            continue
        
        if int(selection) == 0:
            print("Returning to main menu")
            break

        if int(selection) < 0 or int(selection) > len(movies):
            print("Out of bounds!")
            continue

        movie_options_menu(movies[int(selection) - 1])
        return


def add_movie_menu():
    title = input("Movie title: ")
    year = 0
    while True:
        year_input = input("Release year; ")
        if year_input.isdigit():
            year = year_input
            break
        print("Invalid input")
    director = input("Director: ")

    movie = Movie(title, year, director)
    movie.generate_uuid()

    movie.genre = input("Genre (optional): ")
    movie.synopsis = input("Synopsis (optional): ")

    print("\n\n")
    movie.print_long()

    registry.insert_movie(movie)
    print("Movie added successfully!")
    

registry = MovieRegistry()
while True:
    print("--------------\nWelcome to OfflineMovieDatabase!\n--------------")
    print("1. Top 10 Movies")
    print("2. Search for a movie")
    print("3. Add movie to directory")
    print("4. Exit.")
    print("--------------")
    
    selection = input("Please select an option!\n")
    if not selection.isdigit():
        print("Invalid input")
        continue

    match int(selection):
        case 1:
            movies = registry.get_movies([])
            movies.sort(key = lambda x: x.rating, reverse = True)
            select_movie_menu(movies[:10])
            continue
        case 2:
            selection = input("Search: ")
            filters = selection.split()
            if len(filters) == 0:
                print("Invalid search!")
                continue
            movies = registry.get_movies(filters)
            select_movie_menu(movies)
            continue
        case 3:
            add_movie_menu()
            continue
        case 4:
            registry.close_connection()
            print("Exiting...")
            break
        case 0:
            movie1 = Movie("The Shawshank Redemption", 1994, "Frank Darabont")
            movie1.genre = "Drama"
            movie1.synopsis = "After a banker is sentenced to life in Shawshank Prison, he forms an unlikely friendsship with a seasoned inmate and clings to hope amid cruelty and corruption."
            movie1.rating = 9.3
            movie1.generate_uuid()

            movie2 = Movie("The Godfather", 1972, "Francis Ford Coppola")
            movie2.genre = "Drama"
            movie2.synopsis = "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
            movie2.rating = 9.2
            movie2.generate_uuid()

            movie3 = Movie("The Dark Knight", 2008, "Christopher Nolan")
            movie3.genre = "Superhero"
            movie3.synopsis = "When a menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman, James Gordon and Harvey Dent must work together to put an end to the madness."
            movie3.rating = 9.1
            movie3.generate_uuid()

            registry.insert_movie(movie1)
            registry.insert_movie(movie2)
            registry.insert_movie(movie3)
            continue

    print("Invalid input")
        
