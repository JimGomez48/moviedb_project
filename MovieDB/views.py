"""
This file constitutes the View Layer. It is responsible responding to HTTP
requests and preparing context data for the template layer to present.

The View Layer only knows about the following other system layers
- Action Layer
- Forms Layer
- Template Layer
"""

from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpResponse, Http404
from django.core import exceptions
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from moviedb_project.settings import BASE_DIR
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
        return render(request, 'views/index.html', self.get_context_data())


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
        return render(request, 'views/search_results_view.html', self.get_context_data())


class BrowseBaseView(BaseView):
    RESULTS_PER_PAGE = 20
    MAX_SHOWN_PAGES = 9


class BrowseMovieView(BrowseBaseView):
    def get(self, request, search_term=None, page_num=None):
        view_actions = actions.BrowseMovieViewActions()
        movies_queryset = view_actions.get_movie_query_set(search_term)
        if not movies_queryset.exists():
            raise Http404()
        page = view_actions.get_page(movies_queryset, page_num, self.RESULTS_PER_PAGE)
        page_range = view_actions.get_visible_page_range(page, self.MAX_SHOWN_PAGES)
        base_url = reverse('BrowseMovie')
        self.bind_context_data(
            search_term=search_term,
            # page_header='Browse Movies',
            results_header='Movies',
            page_range=page_range,
            page=page,
            base_url=base_url,
        )
        return render(request, 'views/browse_movie_view.html', self.get_context_data())


class BrowseActorView(BrowseBaseView):
    def get(self, request, search_term=None, page_num=None):
        view_actions = actions.BrowseActorViewActions()
        actors_queryset = view_actions.get_actor_query_set(search_term)
        if not actors_queryset.exists():
            raise Http404()
        page = view_actions.get_page(actors_queryset, page_num, self.RESULTS_PER_PAGE)
        page_range = view_actions.get_visible_page_range(page, self.MAX_SHOWN_PAGES)
        base_url = reverse('BrowseActor')
        self.bind_context_data(
            search_term=search_term,
            results_header='Actors',
            page_range=page_range,
            page=page,
            base_url=base_url,
        )
        return render(request, 'views/browse_actor_view.html', self.get_context_data())


class BrowseDirectorView(BrowseBaseView):
    def get(self, request, search_term=None, page_num=None):
        view_actions = actions.BrowseDirectorViewActions()
        directors_queryset = view_actions.get_director_query_set(search_term)
        if not directors_queryset.exists():
            raise Http404()
        page = view_actions.get_page(directors_queryset, page_num, self.RESULTS_PER_PAGE)
        page_range = view_actions.get_visible_page_range(page, self.MAX_SHOWN_PAGES)
        base_url = reverse('BrowseDirector')
        self.bind_context_data(
            search_term=search_term,
            results_header='Directors',
            page_range=page_range,
            page=page,
            base_url=base_url,
        )
        return render(request, 'views/browse_director_view.html', self.get_context_data())


class MovieDetailView(BaseView):
    def get(self, request, mid):
        view_actions = actions.MovieDetailViewActions()
        try:
            movie_details = view_actions.get_movie_details_full(mid)
        except exceptions.ObjectDoesNotExist:
            raise Http404()
        self.bind_context_data(
            movie=movie_details['movie'],
            avg_user_rating=movie_details['avg_rating'],
            companies=movie_details['companies'],
            actors=movie_details['actors'],
            directors=movie_details['directors'],
            genres=movie_details['genres'],
            reviews=movie_details['reviews'],
        )
        return render(request, 'views/detail_movie_view.html', self.get_context_data())


class ActorDetailView(BaseView):
    def get(self, request, aid):
        view_actions = actions.ActorDetailsViewActions()
        try:
            actor_details = view_actions.get_actor_details_full(aid)
        except exceptions.ObjectDoesNotExist:
            raise Http404()
        self.bind_context_data(
            actor=actor_details['actor'],
            movies=actor_details['movies'],
        )
        return render(request, 'views/detail_actor_view.html', self.get_context_data())


class DirectorDetailView(BaseView):
    def get(self, request, did):
        view_actions = actions.DirectorDetailsViewActions()
        try:
            director_details = view_actions.get_director_details_full(did)
        except exceptions.ObjectDoesNotExist:
            raise Http404()
        self.bind_context_data(
            director=director_details['director'],
            movies=director_details['movies'],
        )
        return render(request, 'views/detail_director_view.html', self.get_context_data())


class AddMovieView(BaseView):
    def post(self, request):
        movie_form = forms.MovieForm(request.POST)
        genre_form = forms.MovieGenreForm(request.POST)
        if movie_form.is_valid() and genre_form.is_valid():
            view_actions = actions.AddMovieViewActions()
            view_actions.save_new_movie(
                movie_data=movie_form.cleaned_data,
                genre_data=genre_form.cleaned_data,
            )
            return redirect('Index')
        self.bind_context_data(
            movie_form=movie_form,
            genre_form=genre_form,
        )
        return render(request, 'views/add_movie_view.html', self.get_context_data())

    def get(self, request, *args, **kwargs):
        movie_form = forms.MovieForm()
        genre_form = forms.MovieGenreForm()
        self.bind_context_data(
            movie_form=movie_form,
            genre_form=genre_form,
        )
        return render(request, 'views/add_movie_view.html', self.get_context_data())


class AddActorDirectorView(BaseView):
    ACTOR_FORM = 'actor'
    DIRECTOR_FORM = 'director'

    def post(self, request):
        actor_form = forms.ActorForm()
        director_form = forms.DirectorForm()
        current_form = self.ACTOR_FORM
        if request.POST['submit'] == 'actor':
            actor_form = forms.ActorForm(request.POST)
            current_form = self.ACTOR_FORM
            if actor_form.is_valid():
                view_actions = actions.AddActorDirectorViewActions()
                view_actions.save_new_actor(actor_form.cleaned_data)
                return redirect('Index')
        elif request.POST['submit'] == 'director':
            director_form = forms.DirectorForm(request.POST)
            current_form = self.DIRECTOR_FORM
            if director_form.is_valid():
                view_actions = actions.AddActorDirectorViewActions()
                view_actions.save_new_director(director_form.cleaned_data)
                return redirect('Index')
        # There were errors. Bind form contexts and render
        self.bind_context_data(
            actor_form = actor_form,
            director_form = director_form,
            active_form = current_form
        )
        return render(request, 'views/add_actor_director_view.html', self.get_context_data())

    def get(self, request, *args, **kwargs):
        actor_form = forms.ActorForm()
        director_form = forms.DirectorForm()
        self.bind_context_data(
            actor_form = actor_form,
            director_form = director_form,
            active_form = self.ACTOR_FORM,
        )
        return render(request, 'views/add_actor_director_view.html', self.get_context_data())


class AddActorToMovieView(BaseView):
    def post(self, request):
        form = forms.ActorToMovieForm(request.POST)
        if form.is_valid():
            view_actions = actions.AddActorToMovieViewActions()
            view_actions.add_actor_to_movie(form.cleaned_data)
            return redirect('Index')
        self.bind_context_data(
            movieactor_form=form
        )
        return render(request, 'views/add_actor_to_movie_view.html', self.get_context_data())

    def get(self, request, *args, **kwargs):
        form = forms.ActorToMovieForm()
        self.bind_context_data(
            movieactor_form=form
        )
        return render(request, 'views/add_actor_to_movie_view.html', self.get_context_data())


class AddDirectorToMovieView(BaseView):
    def post(self, request):
        form = forms.DirectorToMovieForm(request.POST)
        if form.is_valid():
            view_actions = actions.AddDirectorToMovieViewActions()
            view_actions.add_director_to_movie(form.cleaned_data)
            return redirect('Index')
        self.bind_context_data(
            moviedirector_form=form
        )
        return render(request, 'views/add_director_to_movie_view.html', self.get_context_data())

    def get(self, request, *args, **kwargs):
        form = forms.DirectorToMovieForm()
        self.bind_context_data(
            moviedirector_form=form
        )
        return render(request, 'views/add_director_to_movie_view.html', self.get_context_data())

class BrowseReviewView(BaseView):
    def get(self, request):
        # return render(request, 'browse_movie_view.html', context)
        raise Http404()


class WriteReviewView(BaseView):
    def post(self, request, mid=None):
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            view_actions = actions.WriteReviewViewActions()
            view_actions.add_movie_review(review_form.cleaned_data)
            return redirect('Index')
        self.bind_context_data(
            review_form = review_form
        )
        return render(request, 'views/add_review_view.html', self.get_context_data())

    def get(self, request, mid=None):
        initial = {}
        if mid:
            initial['mid'] = mid
        review_form = forms.ReviewForm(initial=initial)
        self.bind_context_data(
            review_form = review_form
        )
        return render(request, 'views/add_review_view.html', self.get_context_data())


class ViewReviewView(BaseView):
    def get(self, request, mid=None):
        # return render(request, 'browse_movie_view.html', context)
        raise Http404()