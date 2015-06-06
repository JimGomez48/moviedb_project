from django.conf.urls import url

import views

urlpatterns = [
    # Base
    url(r'^$', views.IndexView.as_view(), name='Index'),
    url(r'^SearchResults/$', views.SearchResultsView.as_view(), name='SearchResults'),
    url(r'^SearchResults/(?P<search_term>[\w+\s+]+)/$', views.SearchResultsView.as_view(), name='SearchResults'),
    # Browse Movie
    url(r'^BrowseMovie/$', views.BrowseMovieView.as_view(), name='BrowseMovie'),
    url(r'^BrowseMovie/search_term=(?P<search_term>[\w+\s+]+)/$', views.BrowseMovieView.as_view(), name='BrowseMovie'),
    url(r'^BrowseMovie/page=(?P<page_num>\d+)/$', views.BrowseMovieView.as_view(), name='BrowseMovie'),
    url(r'^BrowseMovie/search_term=(?P<search_term>[\w+\s+]+)/page=(?P<page_num>\d+)/$', views.BrowseMovieView.as_view(), name='BrowseMovie'),
    # Browse Actor
    url(r'^BrowseActor/$', views.BrowseActorView.as_view(), name='BrowseActor'),
    url(r'^BrowseActor/search_term=(?P<search_term>[\w+\s+]+)/$', views.BrowseActorView.as_view(), name='BrowseActor'),
    url(r'^BrowseActor/page=(?P<page_num>\d+)/$', views.BrowseActorView.as_view(), name='BrowseActor'),
    url(r'^BrowseActor/search_term=(?P<search_term>[\w+\s+]+)/page=(?P<page_num>\d+)/$', views.BrowseActorView.as_view(), name='BrowseActor'),
    # Browse Director
    url(r'^BrowseDirector/$', views.BrowseDirectorView.as_view(), name='BrowseDirector'),
    url(r'^BrowseDirector/search_term=(?P<search_term>[\w+\s+]+)/$', views.BrowseDirectorView.as_view(), name='BrowseDirector'),
    url(r'^BrowseDirector/page=(?P<page_num>\d+)/$', views.BrowseDirectorView.as_view(), name='BrowseDirector'),
    url(r'^BrowseDirector/search_term=(?P<search_term>[\w+\s+]+)/page=(?P<page_num>\d+)/$', views.BrowseDirectorView.as_view(), name='BrowseDirector'),
    # Detail
    url(r'^MovieDetail/(?P<mid>\d+)/$', views.MovieDetailView.as_view(), name='MovieDetail'),
    url(r'^ActorDetail/(?P<aid>\d+)/$', views.ActorDetailView.as_view(), name='ActorDetail'),
    url(r'^DirectorDetail/(?P<did>\d+)/$', views.DirectorDetailView.as_view(), name='DirectorDetail'),
    # Add
    url(r'^AddMovie/$', views.AddMovieView.as_view(), name='AddMovie'),
    url(r'^AddActorDirector/$', views.AddActorDirectorView.as_view(), name='AddActorDirector'),
    url(r'^AddActorMovie/$', views.AddActorToMovieView.as_view(), name='AddActorMovie'),
    url(r'^AddDirectorMovie/$', views.AddDirectorToMovieView.as_view(), name='AddDirectorMovie'),
    # Review
    url(r'^BrowseReview/$', views.BrowseReviewView.as_view(), name='BrowseReview'),
    url(r'^ViewReview/(?P<mid>\d+)/$', views.ViewReviewView.as_view(), name='ViewReview'),
    url(r'^WriteReview/$', views.WriteReviewView.as_view(), name='WriteReview'),
    url(r'^WriteReview/(?P<mid>\d+)/$', views.WriteReviewView.as_view(), name='WriteReview'),
]
