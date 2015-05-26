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

    def __init__(self):
        super(BaseView, self).__init__()
        self.__context = None

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

    def get_context_data(self, **kwargs):
        if not self.__context:
            self.__context = super(BaseView, self).get_context_data(**kwargs)
        nav_items = self.__get_navbar_elements()
        self.__context['title'] = 'MovieDB'
        self.__context['nav_items'] = nav_items
        return self.__context

    def add_context_data_item(self, item):
        if not self.__context:
            self.__context = super(BaseView, self).get_context_data()
            nav_items = self.__get_navbar_elements()
            self.__context['title'] = 'MovieDB'
            self.__context['nav_items'] = nav_items
        self.__context[item.key] = item.value


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


class BrowseBaseView(BaseView):
    RESULTS_PER_PAGE = 20
    MAX_SHOWN_PAGES = 9

    def init_browse_pagination(self, request):
        self.search_term = ''
        self.page_num = 1
        try:
            self.search_term = request.GET['search_term']
        except MultiValueDictKeyError:
            pass
        try:
            self.page_num = int(request.GET['page'])
        except MultiValueDictKeyError:
            self.page_num = 1

    def get_context_data(self, **kwargs):
        context = super(BrowseBaseView, self).get_context_data(**kwargs)
        if self.search_term:
            context['search_term'] = 'search_term=' + self.search_term + '&'
        return context

    def get_visible_page_range(self, paginator, current_page_num):
        if paginator.num_pages < self.MAX_SHOWN_PAGES:
            pages = range(1, paginator.num_pages + 1)
        else:
            start = max(1, min(paginator.num_pages - self.MAX_SHOWN_PAGES + 1, current_page_num - (self.MAX_SHOWN_PAGES // 2)))
            end = min(paginator.num_pages, start + self.MAX_SHOWN_PAGES - 1)
            pages = range(start, end + 1)
        return pages


class BrowseMovieView(BrowseBaseView):
    def get(self, request, *get_args, **kwargs):
        self.init_browse_pagination(request)
        context = self.get_context_data()
        context['page_header'] = 'Browse Movies'
        context['results_header'] = 'Movies'
        # get the movie results that match the search terms and paginate results
        movies = self.__get_movie_results(str(self.search_term).split())
        paginator = Paginator(movies, self.RESULTS_PER_PAGE)
        try:
            page = paginator.page(self.page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context['page_range'] = self.get_visible_page_range(paginator, self.page_num)
        context['page'] = page
        context['page_url'] = reverse('BrowseMovie')
        return render(request, 'browse_movie.html', context)

    def __get_movie_results(self, search_terms):
        if search_terms is None:
            return Movie.objects.all().order_by('title', 'year').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
        return Movie.objects.filter(q_objects).order_by('title', 'year').values()


class BrowseActorView(BrowseBaseView):
    def get(self, request, *args, **kwargs):
        self.init_browse_pagination(request)
        context = self.get_context_data()
        context['page_header'] = 'Browse Actors'
        context['results_header'] = 'Actors'
        # get the actor results that match the search terms and paginate results
        actors = self.__get_actor_results(str(self.search_term).split())
        paginator = Paginator(actors, self.RESULTS_PER_PAGE)
        try:
            page = paginator.page(self.page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context['page_range'] = self.get_visible_page_range(paginator, self.page_num)
        context['page'] = page
        context['page_url'] = reverse('BrowseActor')
        return render(request, 'browse_actor.html', context)

    def __get_actor_results(self, search_terms):
        if search_terms is None:
            return Actor.objects.all().order_by('last', 'first').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(first__icontains=term)
            q_objects |= Q(last__icontains=term)
        return Actor.objects.filter(q_objects).order_by('last', 'first').values()


class BrowseDirectorView(BrowseBaseView):
    def get(self, request, *args, **kwargs):
        self.init_browse_pagination(request)
        context = self.get_context_data()
        context['page_header'] = 'Browse Directors'
        context['results_header'] = 'Directors'
        # get the actor results that match the search terms and paginate results
        actors = self.__get_director_results(str(self.search_term).split())
        paginator = Paginator(actors, self.RESULTS_PER_PAGE)
        try:
            page = paginator.page(self.page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context['page_range'] = self.get_visible_page_range(paginator, self.page_num)
        context['page'] = page
        context['page_url'] = reverse('BrowseDirector')
        return render(request, 'browse_director.html', context)

    def __get_director_results(self, search_terms):
        if search_terms is None:
            return Director.objects.all().order_by('last', 'first').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(first__icontains=term)
            q_objects |= Q(last__icontains=term)
        return Director.objects.filter(q_objects).order_by('last', 'first').values()


class MovieDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(MovieDetailView, self).get_context_data()
        context['page_header'] = 'Movie Details'
        # return render(request, 'detail.html', context)
        return redirect('Error404')
        context['movie_title'] = None
        context['poster_img'] = None
        context['release_date'] = None
        context['mpaa_rating'] = None
        context['company'] = None
        context['actors'] = None
        context['directors'] = None
        context['avg_user_rating'] = None
        return render(request, 'movie_detail.html', context)


class ActorDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(ActorDetailView, self).get_context_data()
        context['page_header'] = 'Actor Details'
        # return render(request, 'detail.html', context)
        return redirect('Error404')

class DirectorDetailView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(DirectorDetailView, self).get_context_data()
        context['page_header'] = 'Director Details'
        # return render(request, 'detail.html', context)
        return redirect('Error404')

class AddMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddMovieView, self).get_context_data()
        context['page_header'] = 'Add Movies'
        # return render(request, 'browse_movie.html', context)
        return redirect('Error404')

class AddActorDirectorView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorDirectorView, self).get_context_data()
        context['page_header'] = 'Add Actors and Directors'
        # return render(request, 'browse_movie.html', context)
        return redirect('Error404')

class AddActorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorToMovieView, self).get_context_data()
        context['page_header'] = 'Add an Actor to a Movie'
        # return render(request, 'browse_movie.html', context)
        return redirect('Error404')

class AddDirectorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddDirectorToMovieView, self).get_context_data()
        context['page_header'] = 'Add a Director to a Movie'
        # return render(request, 'browse_movie.html', context)
        return redirect('Error404')

class WriteReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(WriteReviewView, self).get_context_data()
        context['page_header'] = 'Write a Movie Review'
        # return render(request, 'browse_movie.html', context)
        return redirect('Error404')

class ViewReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(ViewReviewView, self).get_context_data()
        context['page_header'] = 'View Movie Reviews'
        # return render(request, 'browse_movie.html', context)
        return redirect('Error404')