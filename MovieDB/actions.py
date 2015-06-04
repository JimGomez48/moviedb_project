################################################################################
# This file constitutes the Action Layer. It is responsible for carrying out the
# business logic of the system. It uses models to retrieve and persist data and
# services to carry out external service commands.
#
# The Action Layer only knows about the following other system layers
# - Model Layer
# - Services Layer
################################################################################

import xml.etree.cElementTree as ET
import os
import abc
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q
from django.core import paginator

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
                    # kwargs={'search_term':'', 'page_num': 1}
                )
                navbar.append(nav_item)
        return navbar


class IndexViewActions(AbstractActions):
    pass


class SearchResultsViewActions(AbstractActions):
    RESULTS_PER_PAGE = 15

    def get_search_results_all(self, search_term):
        # search_terms = str(search_term).split()
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
        return movie_manager.filter(q_objects).order_by('title', 'year').values()[:self.RESULTS_PER_PAGE]

    def get_search_results_actors(self, search_term):
        search_terms = str(search_term).split()
        actor_manager = models.Actor.objects
        # AND the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            actor_manager = actor_manager.filter(q_objects)
        return actor_manager.values()[:self.RESULTS_PER_PAGE]

    def get_search_results_directors(self, search_term):
        search_terms = str(search_term).split()
        director_manager = models.Director.objects
        # and the below Q objects together
        for term in search_terms:
            # last like '%term%' OR first like '%term%'
            q_objects = Q(last__icontains=term)
            q_objects |= Q(first__icontains=term)
            director_manager = director_manager.filter(q_objects)
        return director_manager.values()[:self.RESULTS_PER_PAGE]


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
    def get_movie_details_full(self, movie_id):
        manager = models.Movie.objects
        movie_details = manager.get_movie_details_full(movie_id)
        return movie_details
