import uuid

class Review:
    def __init__(self, author, rating, movie_id):
        self.author = author
        self.rating = rating
        self.movie_id = movie_id
        
        self.review_text = ""
        self.review_uuid = ""
    
    def generate_uuid(self):
        self.review_uuid = uuid.uuid4().hex

    def get_star_rating(self):
        return "★" * int(self.rating) + "☆" * (10 - int(self.rating))
    
    def print_review(self):
        stars = self.get_star_rating()
        print(f"By {self.author} | {stars} ({self.rating:.1f})")
        if self.review_text != "":
            print(self.review_text)
