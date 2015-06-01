import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q, Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import TemplateView
import xml.etree.cElementTree as ET

from moviedb_project.settings import BASE_DIR
from MovieDB import models
from MovieDB import services


PROJECT_ROOT = BASE_DIR


def Error404(request):
    return render(request, '404.html')


class BaseView(TemplateView):
    def __init__(self):
        super(BaseView, self).__init__()
        self.__context = None

    def get_context_data(self, **kwargs):
        if not self.__context:
            self.__context = super(BaseView, self).get_context_data(**kwargs)
        nav_items = services.get_navbar_data()
        self.__context['title'] = 'MovieDB'
        self.__context['nav_items'] = nav_items
        return self.__context


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
            results = models.Movie.objects.filter(title__icontains=term).values('id', 'title', 'year')
            total_count += results.count()
            movies.extend([item for item in results])
            if total_count >= self.RESULTS_PER_PAGE:
                return movies[0: self.RESULTS_PER_PAGE]
        return movies

    def get_actor_results(self, search_terms):
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

    def get_director_results(self, search_terms):
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
            return models.Movie.objects.all().order_by('title', 'year').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
        return models.Movie.objects.filter(q_objects).order_by('title', 'year').values()


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
            return models.Actor.objects.all().order_by('last', 'first').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(first__icontains=term)
            q_objects |= Q(last__icontains=term)
        return models.Actor.objects.filter(q_objects).order_by('last', 'first').values()


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
            return models.Director.objects.all().order_by('last', 'first').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(first__icontains=term)
            q_objects |= Q(last__icontains=term)
        return models.Director.objects.filter(q_objects).order_by('last', 'first').values()


class MovieDetailView(BaseView):
    def get(self, request, mid):
        context = super(MovieDetailView, self).get_context_data()
        context['page_header'] = 'Movie Details'
        movie = get_object_or_404(models.Movie, id=mid)
        context['movie'] = movie
        manager = models.Movie.objects
        context['genres'] = manager.get_movie_genres(mid)
        context['actors'] = manager.get_movie_actors(mid)
        context['directors'] = manager.get_movie_directors(mid)
        context['avg_user_rating'] = manager.get_movie_average_user_rating(mid)
        return render(request, 'movie_detail.html', context)


class ActorDetailView(BaseView):
    def get(self, request, aid):
        context = super(ActorDetailView, self).get_context_data()
        context['page_header'] = 'Actor Details'
        # return render(request, 'detail.html', context)
        # return redirect('Error404')
        raise Http404()

class DirectorDetailView(BaseView):
    def get(self, request, did):
        context = super(DirectorDetailView, self).get_context_data()
        context['page_header'] = 'Director Details'
        # return render(request, 'detail.html', context)
        raise Http404()

class AddMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddMovieView, self).get_context_data()
        context['page_header'] = 'Add Movies'
        # return render(request, 'browse_movie.html', context)
        raise Http404()

class AddActorDirectorView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorDirectorView, self).get_context_data()
        context['page_header'] = 'Add Actors and Directors'
        # return render(request, 'browse_movie.html', context)
        raise Http404()

class AddActorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorToMovieView, self).get_context_data()
        context['page_header'] = 'Add an Actor to a Movie'
        # return render(request, 'browse_movie.html', context)
        raise Http404()

class AddDirectorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddDirectorToMovieView, self).get_context_data()
        context['page_header'] = 'Add a Director to a Movie'
        # return render(request, 'browse_movie.html', context)
        raise Http404()

class WriteReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(WriteReviewView, self).get_context_data()
        context['page_header'] = 'Write a Movie Review'
        # return render(request, 'browse_movie.html', context)
        raise Http404()

class ViewReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(ViewReviewView, self).get_context_data()
        context['page_header'] = 'View Movie Reviews'
        # return render(request, 'browse_movie.html', context)
        raise Http404()