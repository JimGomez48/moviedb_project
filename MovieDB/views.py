################################################################################
# This file constitutes the View Layer. It is responsible responding to HTTP
# requests and preparing context data for the template layer to present.
#
# The View Layer only knows about the following other system layers
# - Action Layer
# - Forms Layer
# - Template Layer
################################################################################

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q, Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView

from moviedb_project.settings import BASE_DIR
from MovieDB import models
from MovieDB import actions
from MovieDB import forms


PROJECT_ROOT = BASE_DIR


class BaseView(TemplateView):
    def __init__(self):
        super(BaseView, self).__init__()
        self.__context = super(BaseView, self).get_context_data()
        view_actions = actions.BaseViewActions()
        self.bind_context_data(
            title='MovieDB',
            nav_items=view_actions.get_navbar_data(),
            search_form=forms.NavBarSearchForm(),
        )

    def bind_context_data(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.__context[key] = value

    def get_context_data(self, **kwargs):
        return self.__context


class IndexView(BaseView):
    def get(self, request, *args, **kwargs):
        view_actions = actions.IndexViewActions()
        self.bind_context_data(page_header='MovieDB Landing Page')
        return render(request, 'index.html', self.get_context_data())


class SearchResultsView(BaseView):
    def post(self, request):
        search_form = forms.NavBarSearchForm(request.POST)
        if search_form.is_valid():
            return redirect('SearchResults', search_form.cleaned_data['search_term'])
        else:
            raise Http404()

    def get(self, request, search_term):
        if not search_term:
            raise Http404()
        view_actions = actions.SearchResultsViewActions()
        search_results = view_actions.get_search_results_all(search_term)
        self.bind_context_data(
            page_header='Search Results for "%s"' % (search_term),
            search_term=search_term,
            movie_results=search_results['movies'],
            actor_results=search_results['actors'],
            director_results=search_results['directors'],
        )
        return render(request, 'search_results.html', self.get_context_data())


class BrowseBaseView(BaseView):
    RESULTS_PER_PAGE = 20
    MAX_SHOWN_PAGES = 9


class BrowseMovieView(BrowseBaseView):
    def get(self, request, search_term=None, page_num=None):
        view_actions = actions.BrowseMovieViewActions()
        movies_queryset = view_actions.get_movie_query_set(search_term)
        page = view_actions.get_page(movies_queryset, page_num, self.RESULTS_PER_PAGE)
        page_range = view_actions.get_visible_page_range(page, self.MAX_SHOWN_PAGES)
        base_url = reverse('BrowseMovie')
        self.bind_context_data(
            search_term=search_term,
            page_header='Browse Movies',
            results_header='Movies',
            page_range=page_range,
            page=page,
            base_url=base_url,
        )
        return render(request, 'browse_movie.html', self.get_context_data())


class BrowseActorView(BrowseBaseView):
    def get(self, request, search_term=None, page_request=None):
        view_actions = actions.BrowseActorViewActions()
        context = self.get_context_data()
        context['search_term'] = search_term
        context['page_header'] = 'Browse Actors'
        context['results_header'] = 'Actors'
        search_terms = None
        if search_term:
            search_terms = search_term.split()
        # get the actor results that match the search terms and paginate results
        actors = self.__get_actor_results(search_terms)
        paginator = Paginator(actors, self.RESULTS_PER_PAGE)
        try:
            page = paginator.page(page_request)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context['page_range'] = view_actions.get_visible_page_range(paginator, page.number, self.MAX_SHOWN_PAGES)
        context['page'] = page
        context['base_url'] = reverse('BrowseActor')
        return render(request, 'browse_actor.html', context)

    def __get_actor_results(self, search_terms):
        if not search_terms or len(search_terms) < 1:
            return models.Actor.objects.all().order_by('last', 'first').values()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(first__icontains=term)
            q_objects |= Q(last__icontains=term)
        return models.Actor.objects.filter(q_objects).order_by('last', 'first').values()


class BrowseDirectorView(BrowseBaseView):
    def get(self, request, search_term=None, page_request=None):
        view_actions = actions.BrowseDirectorViewActions()
        context = self.get_context_data()
        context['search_term'] = search_term
        context['page_header'] = 'Browse Directors'
        context['results_header'] = 'Directors'
        search_terms = None
        if search_term:
            search_terms = search_term.split()
        # get the actor results that match the search terms and paginate results
        actors = self.__get_director_results(search_terms)
        paginator = Paginator(actors, self.RESULTS_PER_PAGE)
        try:
            page = paginator.page(page_request)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context['page_range'] = view_actions.get_visible_page_range(paginator, page.number, self.MAX_SHOWN_PAGES)
        context['page'] = page
        context['base_url'] = reverse('BrowseDirector')
        return render(request, 'browse_director.html', context)

    def __get_director_results(self, search_terms):
        if not search_terms or len(search_terms) < 1:
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
        view_actions = actions.MovieDetailViewActions()
        details = view_actions.get_movie_details_full(movie_id=mid)
        context['actors'] = details['actors']
        context['directors'] = details['directors']
        context['genres'] = details['genres']
        context['reviews'] = details['reviews']
        context['avg_user_rating'] = details['avg_rating']
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