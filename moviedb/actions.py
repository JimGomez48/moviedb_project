"""
This file constitutes the Action Layer. It is responsible for carrying out the
business logic of the system. It uses models to retrieve and persist data and
services to carry out external service commands.

There is a one-to-one mapping for concrete view classes in the View Layer and
concrete action classes in the Action Layer.

The Action Layer only knows about the following other system layers
- Model Layer
- Services Layer
"""

import abc

from django.core import paginator
from django.db.models import Avg, Q
from django.urls import NoReverseMatch, reverse

from moviedb import models
from moviedb.navbar import NAVBAR


class AbstractActions(metaclass=abc.ABCMeta):
    pass


class BaseViewActions(AbstractActions):
    class NavElement:
        DROPDOWN = "dropdown"
        ITEM = "item"

        def __init__(self, type):
            self.type = type
            self.children = None
            self.text = None
            self.url = None

        def add_child(self, child):
            if child:
                if not self.children:
                    self.children = []
                self.children.append(child)

    def get_navbar_data(self):
        navbar = []
        for entry in NAVBAR:
            if entry["type"] == self.NavElement.DROPDOWN:
                dropdown = self.NavElement(type=self.NavElement.DROPDOWN)
                dropdown.text = entry["text"]
                for item in entry["items"]:
                    nav_item = self.NavElement(type=self.NavElement.ITEM)
                    nav_item.text = item["text"]
                    try:
                        nav_item.url = reverse(item["viewname"])
                    except NoReverseMatch:
                        nav_item.url = "#"
                    dropdown.add_child(nav_item)
                navbar.append(dropdown)
            elif entry["type"] == self.NavElement.ITEM:
                nav_item = self.NavElement(type=self.NavElement.ITEM)
                nav_item.text = entry["text"]
                nav_item.url = reverse(entry["viewname"])
                navbar.append(nav_item)
        return navbar


class IndexViewActions(AbstractActions):
    pass


class SearchResultsViewActions(AbstractActions):
    RESULTS_PER_PAGE = 15

    def get_search_results_all(self, search_term):
        movies = self.get_search_results_movies(search_term)
        actors = self.get_search_results_actors(search_term)
        directors = self.get_search_results_directors(search_term)
        results = {
            "movies": movies,
            "actors": actors,
            "directors": directors,
        }
        return results

    def get_search_results_movies(self, search_term):
        search_terms = str(search_term).split()
        # AND the search_terms together
        q_objects = Q()
        for term in search_terms:
            q_objects &= Q(title__icontains=term)
        movie_manager = models.Movie.objects
        return movie_manager.filter(q_objects).order_by("title", "year")[
            : self.RESULTS_PER_PAGE
        ]

    def get_search_results_actors(self, search_term):
        search_terms = str(search_term).split()
        actor_manager = models.Actor.objects
        # AND the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            actor_manager = actor_manager.filter(q_objects)
        return actor_manager[: self.RESULTS_PER_PAGE]

    def get_search_results_directors(self, search_term):
        search_terms = str(search_term).split()
        director_manager = models.Director.objects
        # and the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            director_manager = director_manager.filter(q_objects)
        return director_manager[: self.RESULTS_PER_PAGE]


class AbstractPaginatedViewActions(AbstractActions):
    def get_visible_page_range(self, page, max_shown_pages=9):
        paginator = page.paginator
        if paginator.num_pages < max_shown_pages:
            pages = range(1, paginator.num_pages + 1)
        else:
            start = max(
                1,
                min(
                    paginator.num_pages - max_shown_pages + 1,
                    page.number - (max_shown_pages // 2),
                ),
            )
            end = min(paginator.num_pages, start + max_shown_pages - 1)
            pages = range(start, end + 1)
        return pages

    def get_page(self, query_set, page_num, results_per_page):
        pager = paginator.Paginator(query_set, results_per_page)
        try:
            page = pager.page(page_num)
        except paginator.PageNotAnInteger:
            page = pager.page(1)
        except paginator.EmptyPage:
            page = pager.page(pager.num_pages)
        return page


class BrowseMovieViewActions(AbstractPaginatedViewActions):
    def get_movie_query_set(self, search_term):
        if not search_term:
            return models.Movie.objects.order_by("title", "year")
        search_terms = str(search_term).split()
        q_objects = Q()
        for term in search_terms:
            q_objects &= Q(title__icontains=term)
        return models.Movie.objects.filter(q_objects).order_by("title", "year")


class BrowseActorViewActions(AbstractPaginatedViewActions):
    def get_actor_query_set(self, search_term):
        actor_manager = models.Actor.objects
        if not search_term:
            return actor_manager.order_by("last", "first")
        search_terms = str(search_term).split()
        # AND the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            actor_manager = actor_manager.filter(q_objects)
        return actor_manager.order_by("last", "first")


class BrowseDirectorViewActions(AbstractPaginatedViewActions):
    def get_director_query_set(self, search_term):
        director_manager = models.Director.objects
        if not search_term:
            return director_manager.order_by("last", "first")
        search_terms = str(search_term).split()
        # AND the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            director_manager = director_manager.filter(q_objects)
        return director_manager.order_by("last", "first")


class MovieDetailViewActions(AbstractActions):
    def get_movie(self, movie_id):
        return models.Movie.objects.get(id=movie_id)

    def get_movie_genres(self, movie_id):
        movie = models.Movie.objects.get(id=movie_id)
        return movie.genres.values_list("value", flat="True")

    def get_movie_actors(self, movie_id):
        movie_actors = (
            models.MovieActor.objects.filter(movie_id=movie_id)
            .select_related("actor")
            .order_by("actor__last", "actor__first")
        )
        return movie_actors

    def get_movie_directors(self, movie_id):
        manager = models.MovieDirector.objects
        results = (
            manager.filter(movie_id=movie_id)
            .select_related("director")
            .order_by("director__last", "director__first")
        )
        return results

    def get_movie_companies(self, movie_id):
        movie = models.Movie.objects.get(id=movie_id)
        return movie.companies.values()

    def get_movie_reviews(self, movie_id):
        manager = models.Review.objects
        return manager.filter(movie_id=movie_id).order_by("-time")[0:3]

    def get_movie_avg_user_rating(self, movie_id):
        manager = models.Review.objects
        return manager.filter(movie_id=movie_id).aggregate(Avg("rating"))["rating__avg"]

    def get_movie_details_full(self, movie_id):
        movie = self.get_movie(movie_id)
        avg_rating = movie.avg_user_rating()
        companies = movie.companies.all()
        cast = models.MovieActor.objects.filter(movie_id=movie_id).select_related(
            "actor"
        )
        # cast = []
        # for movie_actor in models.MovieActor.objects.filter(movie_id=movie_id).select_related('actor'):
        #     cast.append({
        #         'id': movie_actor.actor.id,
        #         'last': movie_actor.actor.last,
        #         'first': movie_actor.actor.first,
        #         'sex': movie_actor.actor.sex,
        #         'dob': movie_actor.actor.dob,
        #         'dod': movie_actor.actor.dod,
        #         'roles': movie_actor.roles(),
        #     })
        directors = movie.directors.all()
        genres = movie.genres.all()
        reviews = movie.review_set.all()
        return {
            "movie": movie,
            "avg_rating": avg_rating,
            "companies": companies,
            "actors": cast,
            "directors": directors,
            "genres": genres,
            "reviews": reviews,
        }

    def add_actor_to_movie(self, data):
        # TODO
        pass

    def add_director_to_movie(self, data):
        # TODO
        pass

    def add_movie_review(self, data):
        # TODO
        pass


class ActorDetailsViewActions(AbstractActions):
    def get_actor_details_full(self, actor_id):
        actor = self.get_actor(actor_id)
        movies = self.get_actor_movies(actor_id)
        return {
            "actor": actor,
            "movies": movies,
        }

    def get_actor(self, actor_id):
        return models.Actor.objects.get(id=actor_id)

    def get_actor_movies(self, actor_id):
        manager = models.MovieActor.objects
        results = (
            manager.filter(actor_id=actor_id)
            .select_related(
                "movie",
            )
            .order_by("-movie__year", "movie__title")
        )
        return results


class DirectorDetailsViewActions(AbstractActions):
    def get_director_details_full(self, director_id):
        director = self.get_director(director_id)
        movies = self.get_director_movies(director_id)
        return {
            "director": director,
            "movies": movies,
        }

    def get_director(self, director_id):
        return models.Director.objects.get(id=director_id)

    def get_director_movies(self, director_id):
        manager = models.MovieDirector.objects
        results = (
            manager.filter(director_id=director_id)
            .select_related(
                "movie",
            )
            .order_by("-movie__year", "movie__title")
        )
        return results


class AddMovieViewActions(AbstractActions):
    def save_new_movie(self, **kwargs):
        movie_data = kwargs["movie_data"]
        genre_data = kwargs["genre_data"]
        movie = self.__save_movie_model(movie_data)
        self.__save_movie_genre_models(movie, genre_data["genres"])

    def __save_movie_model(self, movie_data):
        movie = models.Movie()
        movie.title = movie_data["title"]
        movie.year = movie_data["year"]
        movie.mpaa_rating = movie_data["mpaa_rating"]
        movie.save()
        return movie

    def __save_movie_genre_models(self, movie, genres):
        for genre in genres:
            movie_genre = models.MovieGenre()
            movie_genre.movie = movie
            movie_genre.genre = models.Genre.objects.get(value=genre)
            movie_genre.save()


class AddActorDirectorViewActions(AbstractActions):
    def save_new_actor(self, actor_data):
        actor = models.Actor()
        actor.last = actor_data["last"]
        actor.first = actor_data["first"]
        actor.sex = models.Actor.Sex(actor_data["sex"])  # ValueError if invalid
        actor.dob = actor_data["dob"]
        if actor_data["dod"]:
            actor.dod = actor_data["dod"]
        else:
            actor.dod = None
        actor.save()

    def save_new_director(self, director_data):
        director = models.Director()
        director.last = director_data["last"]
        director.first = director_data["first"]
        director.dob = director_data["dob"]
        if director_data["dod"]:
            director.dod = director_data["dod"]
        else:
            director.dod = None
        director.save()


class AddActorToMovieViewActions(AbstractActions):
    def add_actor_to_movie(self, data):
        movie_actors = models.MovieActor.objects
        movie_actors.create(
            movie=data["movie"],
            actor=data["actor"],
        )


class AddDirectorToMovieViewActions(AbstractActions):
    def add_director_to_movie(self, data):
        movie_directors = models.MovieDirector.objects
        movie_directors.create(
            movie=data["movie"],
            director=data["director"],
        )


class WriteReviewViewActions(AbstractActions):
    def add_movie_review(self, data):
        reviews = models.Review.objects
        reviews.create(
            user_name=data["user_name"],
            movie=data["movie"],
            rating=data["rating"],
            comment=data["comment"],
        )
