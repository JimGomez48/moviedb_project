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

import xml.etree.cElementTree as ET
import os
import abc
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import connection
from django.db.models import Q, Avg
from django.core import paginator
from django.core import exceptions

from moviedb_project.settings import BASE_DIR
from MovieDB import models
from MovieDB import services


class AbstractActions(object):
    __metaclass__ = abc.ABCMeta


class BaseViewActions(AbstractActions):
    class NavElement(object):
        DROPDOWN = 'dropdown'
        ITEM = 'item'

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
        # parse navbar.xml to get the navbar information
        navbar = []
        path = os.path.join(BASE_DIR, 'MovieDB/static/data/navbar.xml')
        tree = ET.parse(path)
        root = tree.getroot()
        for element in root:
            if element.tag == 'dropdown':
                dropdown = self.NavElement(type=self.NavElement.DROPDOWN)
                dropdown.text = element.attrib['name']
                for sub_element in element:
                    nav_item = self.NavElement(type=self.NavElement.ITEM)
                    nav_item.text = sub_element.find('text').text
                    try:
                        nav_item.url = reverse(
                            str(sub_element.find('viewname').text),
                            # kwargs={'search_term':None, 'page_num': 1}
                        )
                    except NoReverseMatch:
                        nav_item.url = '#'
                    dropdown.add_child(nav_item)
                navbar.append(dropdown)
            elif element.tag == 'item':
                nav_item = self.NavElement(type=self.NavElement.ITEM)
                nav_item.text = element.find('text').text
                nav_item.url = reverse(
                    str(element.find('viewname').text),
                )
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
            'movies': movies,
            'actors': actors,
            'directors': directors,
        }
        return results

    def get_search_results_movies(self, search_term):
        search_terms = str(search_term).split()
        # AND the search_terms together
        q_objects = Q()
        for term in search_terms:
            q_objects &= Q(title__icontains=term)
        movie_manager = models.Movie.objects
        return movie_manager.filter(q_objects).order_by('title', 'year')[:self.RESULTS_PER_PAGE]

    def get_search_results_actors(self, search_term):
        search_terms = str(search_term).split()
        actor_manager = models.Actor.objects
        # AND the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            actor_manager = actor_manager.filter(q_objects)
        return actor_manager[:self.RESULTS_PER_PAGE]

    def get_search_results_directors(self, search_term):
        search_terms = str(search_term).split()
        director_manager = models.Director.objects
        # and the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            director_manager = director_manager.filter(q_objects)
        return director_manager[:self.RESULTS_PER_PAGE]


class AbstractPaginatedViewActions(AbstractActions):
    __metaclass__ = abc.ABCMeta

    def get_visible_page_range(self, page, max_shown_pages=9):
        paginator = page.paginator
        if paginator.num_pages < max_shown_pages:
            pages = range(1, paginator.num_pages + 1)
        else:
            start = max(1, min(paginator.num_pages - max_shown_pages + 1, page.number - (max_shown_pages // 2)))
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
            return models.Movie.objects.order_by('title', 'year')
        search_terms = str(search_term).split()
        q_objects = Q()
        for term in search_terms:
            q_objects &= Q(title__icontains=term)
        return models.Movie.objects.filter(q_objects).order_by('title', 'year')


class BrowseActorViewActions(AbstractPaginatedViewActions):
    def get_actor_query_set(self, search_term):
        actor_manager = models.Actor.objects
        if not search_term:
            return actor_manager.order_by('last', 'first')
        search_terms = str(search_term).split()
        # AND the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            actor_manager = actor_manager.filter(q_objects)
        return actor_manager.order_by('last', 'first')


class BrowseDirectorViewActions(AbstractPaginatedViewActions):
    def get_director_query_set(self, search_term):
        director_manager = models.Director.objects
        if not search_term:
            return director_manager.order_by('last', 'first')
        search_terms = str(search_term).split()
        # AND the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            director_manager = director_manager.filter(q_objects)
        return director_manager.order_by('last', 'first')


class MovieDetailViewActions(AbstractActions):
    def get_movie(self, movie_id):
        return models.Movie.objects.get(id=movie_id)

    def get_movie_genres(self, movie_id):
        manager = models.MovieGenre.objects
        return manager.filter(movie_id=movie_id).values_list('genre',
                                                             flat='True')

    def get_movie_actors(self, movie_id):
        query_set = models.MovieActor.objects
        query_set = query_set.filter(movie_id=movie_id).select_related(
            'actor__id',
            'actor__last',
            'actor__first',
            'actor__sex',
            'actor__dob',
            'actor__dod',
        ).order_by('actor__last', 'actor__first')
        return query_set

    def get_movie_directors(self, movie_id):
        manager = models.MovieDirector.objects
        results = manager.filter(movie_id=movie_id).select_related(
            'director__id',
            'director__last',
            'director__first',
            'director__dob',
            'director__dod',
        ).order_by('director__last', 'director__first')
        return results

    def get_movie_reviews(self, movie_id):
        manager = models.Review.objects
        return manager.filter(movie_id=movie_id).order_by('-time')[0:3]

    def get_movie_avg_user_rating(self, movie_id):
        manager = models.Review.objects
        return manager.filter(movie_id=movie_id).aggregate(Avg('rating'))[
            'rating__avg']

    def get_movie_details_full(self, movie_id):
        movie = self.get_movie(movie_id)
        actors = self.get_movie_actors(movie_id)
        directors = self.get_movie_directors(movie_id)
        genres = self.get_movie_genres(movie_id)
        reviews = self.get_movie_reviews(movie_id)
        avg_rating = self.get_movie_avg_user_rating(movie_id)
        return {
            'movie': movie,
            'actors': actors,
            'directors': directors,
            'genres': genres,
            'reviews': reviews,
            'avg_rating': avg_rating,
        }

    def get_movie_details_full_sproc(self, movie_id):
        proc_name = 'movie_db.sp_get_movie_details_full'
        with connection.cursor() as cursor:
            cursor.callproc(proc_name, [movie_id])
            results = {}
            # get actors
            actors = []
            for row in cursor:
                actor = models.Actor()
                actor.id =      row[0]
                actor.last =    row[1]
                actor.first =   row[2]
                actor.sex =     row[3]
                actor.dob =     row[4]
                actor.dod =     row[5]
                actor.role =    row[6]
                actors.append(actor)
            results['actors'] = actors
            # get directors
            cursor.nextset()
            directors = []
            for row in cursor:
                director = models.Director()
                director.id =       row[0]
                director.last =     row[1]
                director.first =    row[2]
                director.dob =      row[3]
                director.dod =      row[4]
                directors.append(director)
            results['directors'] = directors
            # get genres
            cursor.nextset()
            genres = []
            for row in cursor:
                genres.append(row[0])
            results['genres'] = genres
            # get reviews
            cursor.nextset()
            reviews = []
            for row in cursor:
                review = models.Review()
                review.id =         row[0]
                review.time =       row[1]
                review.user_name =  row[2]
                review.rating =     row[3]
                review.comment =    row[4]
                reviews.append(review)
            results['reviews'] = reviews
            # get average review rating
            cursor.nextset()
            results['avg_rating'] = cursor.fetchone()[0]
        return results

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
            'actor': actor,
            'movies': movies,
        }

    def get_actor(self, actor_id):
        return models.Actor.objects.get(id=actor_id)

    def get_actor_movies(self, actor_id):
        manager = models.MovieActor.objects
        results = manager.filter(aid=actor_id).select_related(
            'mid__id',
            'mid__title',
            'mid__year',
            'mid__rating',
            'mid__company',
        ).order_by('-mid__year', 'mid__title')
        return results


class DirectorDetailsViewActions(AbstractActions):
    def get_director_details_full(self, director_id):
        director = self.get_director(director_id)
        movies = self.get_director_movies(director_id)
        return {
            'director': director,
            'movies': movies,
        }

    def get_director(self, director_id):
        return models.Director.objects.get(id=director_id)

    def get_director_movies(self, director_id):
        manager = models.MovieDirector.objects
        results = manager.filter(did=director_id).select_related(
            'mid__id',
            'mid__title',
            'mid__year',
            'mid__rating',
            'mid__company',
        ).order_by('-mid__year', 'mid__title')
        return results


class AddMovieViewActions(AbstractActions):
    def save_new_movie(self, **kwargs):
        movie_data = kwargs['movie_data']
        genre_data = kwargs['genre_data']
        movie = self.__save_movie_model(movie_data)
        self.__save_movie_genre_models(movie, genre_data.values()[0])

    def __save_movie_model(self, movie_data):
        movie = models.Movie()
        movie.title = movie_data['title']
        movie.company = movie_data['company']
        movie.year = movie_data['year']
        movie.rating = movie_data['rating']
        movie.save()
        return movie

    def __save_movie_genre_models(self, movie, genres):
        for genre in genres:
            movie_genre = models.MovieGenre()
            movie_genre.movie = movie
            movie_genre.genre = genre
            movie_genre.save()


class AddActorDirectorViewActions(AbstractActions):
    def save_new_actor(self, actor_data):
        actor = models.Actor()
        actor.last = actor_data['last']
        actor.first = actor_data['first']
        if actor_data['sex'] == models.Actor.MALE:
            actor.sex = models.Actor.MALE
        elif actor_data['sex'] == models.Actor.FEMALE:
            actor.sex = models.Actor.FEMALE
        else:
            raise ValueError('Invalid value for actor.sex')
        actor.dob = actor_data['dob']
        if actor_data['dod']:
            actor.dod = actor_data['dod']
        else:
            actor.dod = None
        actor.save()

    def save_new_director(self, director_data):
        director = models.Director()
        director.last = director_data['last']
        director.first = director_data['first']
        director.dob = director_data['dob']
        if director_data['dod']:
            director.dod = director_data['dod']
        else:
            director.dod = None
        director.save()


class AddActorToMovieViewActions(AbstractActions):
    def add_actor_to_movie(self, data):
        movie_actors = models.MovieActor.objects
        movie_actors.create(
            mid=data['mid'],
            aid=data['aid'],
            role=data['role'],
        )


class AddDirectorToMovieViewActions(AbstractActions):
    def add_director_to_movie(self, data):
        movie_directors = models.MovieDirector.objects
        movie_directors.create(
            mid=data['mid'],
            did=data['did'],
        )


class WriteReviewViewActions(AbstractActions):
    def add_movie_review(self, data):
        reviews = models.Review.objects
        reviews.create(
            user_name=data['user_name'],
            mid=data['mid'],
            rating=data['rating'],
            comment=data['comment'],
        )