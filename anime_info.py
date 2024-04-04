class AnimeInfo:
    def __init__(self, name, rating, release_date):
        self.name = name
        self.rating = rating
        self.release_date = release_date

    def __str__(self):
        return f"{self.name} ({self.release_date}): {self.rating}"
