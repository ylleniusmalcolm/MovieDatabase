import sqlite3
from movie import Movie
from review import Review

class MovieRegistry:
    def __init__(self):
        self.connection = sqlite3.connect("movie_database.db")
        cursor = self.connection.cursor()

        create_movies_query = '''
        CREATE TABLE IF NOT EXISTS Movies (
            uuid TEXT PRIMARY KEY NOT NULL,
            title TEXT NOT NULL,
            year INTEGER,
            director TEXT,
            genre TEXT,
            synopsis TEXT,
            rating REAL
        );
        '''

        create_reviews_query= '''
        CREATE TABLE IF NOT EXISTS Reviews (
            uuid TEXT PRIMARY KEY NOT NULL,
            movieID TEXT NOT NULL,
            author TEXT,
            rating REAL,
            review TEXT
        );
        '''

        cursor.execute(create_movies_query)
        cursor.execute(create_reviews_query)
        self.connection.commit()

        print("Table 'Movies' created successfully!")


    def close_connection(self):
        self.connection.close()

    
    def insert_movie(self, movie):
        cursor = self.connection.cursor()

        insert_query = '''
        INSERT INTO Movies (uuid, title, year, director, genre, synopsis, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        '''
        movie_data = (movie.movie_uuid, movie.title, movie.year, movie.director, movie.genre, movie.synopsis, movie.rating)

        cursor.execute(insert_query, movie_data)
        self.connection.commit()

        print("Added " + movie.title + " succesfully!")


    def get_movies(self, filters):
        cursor = self.connection.cursor()

        select_query = "SELECT * FROM Movies;"
        cursor.execute(select_query)

        movies_data = cursor.fetchall()
        movies = []
        
        for movie_data in movies_data:
            movies.append(self.movie_from_data(movie_data))

        if len(filters) == 0:
            return movies

        filtered_movies = []

        #Case insensitive word check for title and director
        #Numerical check for year
        for movie in movies:
            include_movie = True
            for filter_word in filters:
                contains_filter = False
                if filter_word.lower() in movie.title.lower():
                    contains_filter = True
                elif filter_word.lower() in movie.director.lower():
                    contains_filter = True
                elif filter_word.isdigit() and year == filter_word:
                    contains_filter = True

                if not contains_filter:
                    include_movie = False
                    break
            if include_movie:
                filtered_movies.append(movie)
        return filtered_movies
    

    def movie_from_data(self, movie_data):
        title = movie_data[1]
        year = movie_data[2]
        director = movie_data[3]

        movie = Movie(title, year, director)
        movie.genre = movie_data[4]
        movie.synopsis = movie_data[5]
        movie.rating = movie_data[6]
        movie.movie_uuid = movie_data[0]

        return movie


    def add_review(self, review):
        cursor = self.connection.cursor()

        insert_query = '''
        INSERT INTO Reviews (uuid, movieID, author, rating, review)
        VALUES (?, ?, ?, ?, ?);
        '''
        review_data = (review.review_uuid, review.movie_id, review.author, review.rating, review.review_text)

        cursor.execute(insert_query, review_data)
        self.connection.commit()

        self.update_rating(review.movie_id)
        print("Added review succesfully!")

    
    def get_reviews(self, movie_id):
        cursor = self.connection.cursor()

        select_query = "SELECT * FROM Reviews"
        cursor.execute(select_query)
        reviews_data = cursor.fetchall()
        reviews = []

        for review_data in reviews_data:
            if review_data[1] == movie_id:
                reviews.append(self.review_from_data(review_data))

        return reviews
        

    def review_from_data(self, review_data):
        movie_id = review_data[1]
        author = review_data[2]
        rating = review_data[3]

        review = Review(author, rating, movie_id)
        review.review_uuid = review_data[0]
        review.review_text = review_data[4]

        return review


    def update_rating(self, movie_id):
        reviews = self.get_reviews(movie_id)
        new_rating = 0
        if len(reviews) != 0:
            for review in reviews:
                new_rating += review.rating
            new_rating /= len(reviews)

        cursor = self.connection.cursor()
        
        update_query = '''
        UPDATE Movies 
        SET rating = ? 
        WHERE uuid = ?;
        '''

        cursor.execute(update_query, (new_rating, movie_id))
        self.connection.commit()
