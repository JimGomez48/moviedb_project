from django.db.models import Manager
from MovieDB.models import Movie
from MovieDB.models import Actor
from MovieDB.models import Director
from MovieDB.models import MovieActor
from MovieDB.models import MovieDirector
from MovieDB.models import MovieGenre


class MovieManager(Manager):
    def get_movie_genres(self, movie_id):
        manager = MovieGenre.objects
        manager.filter(movie=movie_id)
        return manager.values('genre')

    def get_movie_actors(self, movie_id):
        manager = MovieActor.objects
        manager.filter(movie=movie_id)

    def get_movie_directors(self, movie_id):
        pass

    def get_movie_reviews(self, movie_id):
        pass

class ActorManager(Manager):
    def get_actor_movies(self, movie_id):
        pass

class DirectorManager(Manager):
    pass

class ReviewManager(Manager):
    pass
