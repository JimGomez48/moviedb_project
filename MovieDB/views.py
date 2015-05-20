import os
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from django.views.generic.base import TemplateView
import xml.etree.cElementTree as ET
from MovieDB.models import *

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def Error404(request):
    return render(request, '404.html')


class BaseView(TemplateView):
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

    def get_context_data(self, **kwargs):
        nav_items = self.__get_navbar_elements()
        context = {
            'title': 'MovieDB',
            'nav_items': nav_items,
        }
        return context

    def __get_navbar_elements(self):
        # parse navbar.xml to get the navbar information
        navbar = []
        tree = ET.parse(PROJECT_ROOT + '/data/navbar.xml')
        root = tree.getroot()
        for element in root:
            if element.tag == 'dropdown':
                dropdown = self.NavElement(type=self.NavElement.DROPDOWN)
                dropdown.text = element.attrib['name']
                for sub_element in element:
                    nav_item = self.NavElement(type=self.NavElement.ITEM)
                    nav_item.text = sub_element.find('text').text
                    try:
                        nav_item.url = reverse(str(sub_element.find('viewname').text))
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


class IndexView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['page_header'] = 'MovieDB Landing Page'
        return render(request, 'index.html', context)


class SearchResultsView(BaseView):
    RESULTS_PER_PAGE = 20

    def get(self, request, *args, **kwargs):
        context = super(SearchResultsView, self).get_context_data()
        context['page_header'] = 'Search Results for "' + request.GET['search_term'] + '"'
        search_terms = str(request.GET['search_term']).split(' ')
        # save search term in GET to pass to browse pages
        # request.session['search_terms'] = search_terms
        # request.GET['search_terms'] = search_terms
        movies = self.get_movie_results(search_terms)
        actors = self.get_actor_results(search_terms)
        directors = self.get_director_results(search_terms)
        context['movie_results'] = movies
        context['actor_results'] = actors
        context['director_results'] = directors
        return render(request, 'search_results.html', context)

    def get_movie_results(self, search_terms):
        movies = []
        total_count = 0
        for term in search_terms:
            results = Movie.objects.filter(title__icontains=term)
            total_count += results.count()
            movies.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return movies[0: self.RESULTS_PER_PAGE]
        return movies

    def get_actor_results(self, search_terms):
        actors = []
        total_count = 0
        for term in search_terms:
            results = Actor.objects.filter(Q(first__icontains=term) | Q(last__icontains=term))
            total_count += results.count()
            actors.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return actors[0: self.RESULTS_PER_PAGE]
        return actors

    def get_director_results(self, search_terms):
        directors = []
        total_count = 0
        for term in search_terms:
            results = Director.objects.filter(Q(first__icontains=term) | Q(last__icontains=term))
            total_count += results.count()
            directors.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return directors[0: self.RESULTS_PER_PAGE]
        return directors


class BrowseMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(BrowseMovieView, self).get_context_data()
        context['page_header'] = 'Browse Movies'
        return render(request, 'browse.html', context)


class BrowseActorView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(BrowseActorView, self).get_context_data()
        context['page_header'] = 'Browse Actors'
        return render(request, 'browse.html', context)

class BrowseDirectorView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(BrowseDirectorView, self).get_context_data()
        context['page_header'] = 'Browse Directors'
        return render(request, 'browse.html', context)


class MovieDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(MovieDetailView, self).get_context_data()
        context['page_header'] = 'Movie Details'
        return render(request, 'detail.html', context)


class ActorDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(ActorDetailView, self).get_context_data()
        context['page_header'] = 'Actor Details'
        return render(request, 'detail.html', context)


class DirectorDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(DirectorDetailView, self).get_context_data()
        context['page_header'] = 'Director Details'
        return render(request, 'detail.html', context)


class AddMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddMovieView, self).get_context_data()
        context['page_header'] = 'Add Movies'
        return render(request, 'browse.html', context)


class AddActorDirectorView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorDirectorView, self).get_context_data()
        context['page_header'] = 'Add Actors and Directors'
        return render(request, 'browse.html', context)


class AddActorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorToMovieView, self).get_context_data()
        context['page_header'] = 'Add an Actor to a Movie'
        return render(request, 'browse.html', context)


class AddDirectorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddDirectorToMovieView, self).get_context_data()
        context['page_header'] = 'Add a Director to a Movie'
        return render(request, 'browse.html', context)


class WriteReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(WriteReviewView, self).get_context_data()
        context['page_header'] = 'Write a Movie Review'
        return render(request, 'browse.html', context)


class ViewReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(ViewReviewView, self).get_context_data()
        context['page_header'] = 'View Movie Reviews'
        return render(request, 'browse.html', context)
