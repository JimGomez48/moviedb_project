import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
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
    RESULTS_PER_PAGE = 15

    def get(self, request, *args, **kwargs):
        context = super(SearchResultsView, self).get_context_data()
        context['page_header'] = 'Search Results for "' + request.GET['search_term'] + '"'
        context['search_term'] = request.GET['search_term']
        search_terms = str(request.GET['search_term']).split(' ')
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
            results = Movie.objects.filter(title__icontains=term).values('id', 'title', 'year')
            total_count += results.count()
            movies.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return movies[0: self.RESULTS_PER_PAGE]
        return movies

    def get_actor_results(self, search_terms):
        actors = []
        total_count = 0
        for term in search_terms:
            results = Actor.objects.filter(Q(first__icontains=term) | Q(last__icontains=term)).values('id', 'last', 'first', 'dob')
            total_count += results.count()
            actors.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return actors[0: self.RESULTS_PER_PAGE]
        return actors

    def get_director_results(self, search_terms):
        directors = []
        total_count = 0
        for term in search_terms:
            results = Director.objects.filter(Q(first__icontains=term) | Q(last__icontains=term)).values('id', 'last', 'first', 'dob')
            total_count += results.count()
            directors.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return directors[0: self.RESULTS_PER_PAGE]
        return directors


class PaginatedView(BaseView):
    MAX_SHOWN_PAGES = 9

    def get_visible_page_range(self, paginator, current_page_num):
        if paginator.num_pages < self.MAX_SHOWN_PAGES:
            pages = range(1, paginator.num_pages + 1)
        else:
            if current_page_num <= (self.MAX_SHOWN_PAGES // 2) + 1:
                start = 1
            else:
                start = current_page_num - (self.MAX_SHOWN_PAGES // 2)
            end = min(paginator.num_pages, start + self.MAX_SHOWN_PAGES - 1)
            pages = range(start, end + 1)
        return pages

    def build_query_string(self, args):
        querystring = ''
        for arg in args:
            if not querystring:
                querystring = '?'
            else:
                querystring += '&'
            querystring += str(arg.key) + '=' + str(arg.value)
        return querystring


class BrowseMovieView(PaginatedView):
    RESULTS_PER_PAGE = 20

    def get(self, request, *get_args, **kwargs):
        context = super(BrowseMovieView, self).get_context_data()
        context['page_header'] = 'Browse Movies'
        context['results_header'] = 'Movies'
        # get the search terms and page num
        try:
            search_term = request.GET['search_term']
            search_terms = str(search_term).split(' ')
        except MultiValueDictKeyError:
            search_term = None
            search_terms = None
        try:
            page_num = int(request.GET['page'])
        except MultiValueDictKeyError:
            page_num = 1
        # get the movie results that match the search terms and paginate results
        movies = self.__get_movie_results(search_terms)
        paginator = Paginator(movies, self.RESULTS_PER_PAGE)
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context['page_range'] = self.get_visible_page_range(paginator, page_num)
        context['page'] = page
        context['page_url'] = reverse('BrowseMovie')
        # query_string = self.build_query_string({
        #     'search_term': search_term,
        #     'page': page.number
        # })
        # context['query_string'] = query_string
        if search_term:
            context['search_term'] = 'search_term=' + search_term + '&'
        return render(request, 'browse_movie.html', context)

    def __get_movie_results(self, search_terms):
        if search_terms is None:
            return Movie.objects.all().order_by('title', 'year').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
        return Movie.objects.filter(q_objects).values()


class BrowseActorView(PaginatedView):
    def get(self, request, *args, **kwargs):
        context = super(BrowseActorView, self).get_context_data()
        context['page_header'] = 'Browse Actors'
        context['results_header'] = 'Actors'
        try:
            search_terms = request.GET['search_term'].split(' ')
        except MultiValueDictKeyError:
            search_terms = None
        context['actors'] = self.__get_actor_results(search_terms)
        context['pages'] = self.get_visible_page_range(paginator, page)
        context['current_page'] = page
        context['page_url'] = reverse('BrowseMovie')
        return render(request, 'browse_actor.html', context)

    def __get_actor_results(self, search_terms):
        if search_terms is None:
            return Actor.objects.all().order_by('last', 'first').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(first__icontains=term)
            q_objects |= Q(last__icontains=term)
        return Actor.objects.filter(q_objects).values()


class BrowseDirectorView(PaginatedView):
    def get(self, request, *args, **kwargs):
        context = super(BrowseDirectorView, self).get_context_data()
        context['page_header'] = 'Browse Directors'
        context['results_header'] = 'Directors'
        try:
            search_terms = request.GET['search_term'].split(' ')
        except MultiValueDictKeyError:
            search_terms = None
        context['directors'] = self.__get_director_results(search_terms)
        context['pages'] = self.get_visible_page_range(paginator, page)
        context['current_page'] = page
        context['page_url'] = reverse('BrowseMovie')
        return render(request, 'browse_director.html', context)

    def __get_director_results(self, search_terms):
        if search_terms is None:
            return Director.objects.all().order_by('last', 'first').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(first__icontains=term)
            q_objects |= Q(last__icontains=term)
        return Director.objects.filter(q_objects).values()


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
        return render(request, 'browse_movie.html', context)


class AddActorDirectorView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorDirectorView, self).get_context_data()
        context['page_header'] = 'Add Actors and Directors'
        return render(request, 'browse_movie.html', context)


class AddActorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorToMovieView, self).get_context_data()
        context['page_header'] = 'Add an Actor to a Movie'
        return render(request, 'browse_movie.html', context)


class AddDirectorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddDirectorToMovieView, self).get_context_data()
        context['page_header'] = 'Add a Director to a Movie'
        return render(request, 'browse_movie.html', context)


class WriteReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(WriteReviewView, self).get_context_data()
        context['page_header'] = 'Write a Movie Review'
        return render(request, 'browse_movie.html', context)


class ViewReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(ViewReviewView, self).get_context_data()
        context['page_header'] = 'View Movie Reviews'
        return render(request, 'browse_movie.html', context)
