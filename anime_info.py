class AnimeInfo:
    def __init__(self, id, name, rating, release_date, news, genres, themes, related):
        self.id = id
        self.name = name
        self.rating = rating
        self.release_date = release_date[0:10]
        self.news = news
        self.genres = genres
        self.themes = themes
        self.related = related

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'release_date': self.release_date,
            'news': self.news,
            'genres': self.genres,
            'themes': self.themes,
            'related': self.related,
        }

    def get_news_count(self):
        return len(self.news)

    def __str__(self):
        return f"[{self.id}]{self.name} ({self.release_date}): {self.rating}, with {self.get_news_count()} appearances"
