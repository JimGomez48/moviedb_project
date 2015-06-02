import xml.etree.cElementTree as ET
import os

from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q

from moviedb_project.settings import BASE_DIR
from MovieDB import models
from MovieDB import forms


class AbstractActions(object):
    def bind_context_data(self, context, **kwargs):
        raise NotImplementedError()


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

    def bind_context_data(self, context, **kwargs):
        context['title'] = 'MovieDB'
        context['nav_items'] = self.__get_navbar_data()
        context['search_form'] = forms.NavBarSearchForm()
        return context

    def __get_navbar_data(self):
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
                            str(sub_element.find('viewname').text))
                    except NoReverseMatch:
                        nav_item.url = ''
                    dropdown.add_child(nav_item)
                navbar.append(dropdown)
            elif element.tag == 'item':
                nav_item = self.NavElement(type=self.NavElement.ITEM)
                nav_item.text = element.find('text').text
                nav_item.url = reverse(str(element.find('viewname').text))
                navbar.append(nav_item)
        return navbar


class IndexViewActions(AbstractActions):
    def bind_context_data(self, context, **kwargs):
        context['page_header'] = 'MovieDB Landing Page'
        return context


class SearchResultsViewActions(AbstractActions):
    RESULTS_PER_PAGE = 15

    def bind_context_data(self, context, **kwargs):
        context['page_header'] = 'Search Results for "' + kwargs['search_term'] + '"'
        context['search_term'] = kwargs['search_term']
        search_terms = str(kwargs['search_term']).split(' ')
        movies = self.__get_movie_results(search_terms)
        actors = self.__get_actor_results(search_terms)
        directors = self.__get_director_results(search_terms)
        context['movie_results'] = movies
        context['actor_results'] = actors
        context['director_results'] = directors
        return context

    def __get_movie_results(self, search_terms):
        movies = []
        total_count = 0
        for term in search_terms:
            results = models.Movie.objects.filter(title__icontains=term).values('id', 'title', 'year')
            total_count += results.count()
            movies.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return movies[0: self.RESULTS_PER_PAGE]
        return movies

    def __get_actor_results(self, search_terms):
        actors = []
        total_count = 0
        for term in search_terms:
            results = models.Actor.objects.filter(
                Q(first__icontains=term) |
                Q(last__icontains=term)).values('id', 'last', 'first', 'dob')
            total_count += results.count()
            actors.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return actors[0: self.RESULTS_PER_PAGE]
        return actors

    def __get_director_results(self, search_terms):
        directors = []
        total_count = 0
        for term in search_terms:
            results = models.Director.objects.filter(
                Q(first__icontains=term) |
                Q(last__icontains=term)).values('id', 'last', 'first', 'dob')
            total_count += results.count()
            directors.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return directors[0: self.RESULTS_PER_PAGE]
        return directors


def get_movie_details_full(movie_id, **kwargs):
    manager = models.Movie.objects
    movie_details = manager.get_movie_details_full(movie_id)
    return movie_details