import uuid

class Movie:
    def __init__(self, title, year, director):
        self.title = title
        self.year = year
        self.director = director

        self.genre = ""
        self.synopsis = ""
        self.rating = 0.0
        self.movie_uuid = ""


    def generate_uuid(self):
        self.movie_uuid = uuid.uuid4().hex


    def print_short(self):
        stars = self.get_star_rating()
        print(f"{self.title} ({self.year}), {self.director}  {stars}")


    def print_long(self):
        stars = self.get_star_rating()
        print(f"{self.title} ({self.year})  Rating:{stars}({self.rating:.1f})")
        print(f"Genre: {self.genre}")
        print(f"Synopsis: {self.synopsis}")


    def get_star_rating(self):
        return "★" * int(self.rating) + "☆" * (10 - int(self.rating))
