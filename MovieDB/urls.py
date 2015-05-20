from django.conf.urls import url

import views

urlpatterns = [
    # Error
    url(r'^404/$', views.Error404, name='Error404'),
    # Base
    url(r'^$', views.IndexView.as_view(), name='Index'),
    url(r'^SearchResults/$', views.SearchResultsView.as_view(), name='SearchResults'),
    # Browse
    url(r'^BrowseMovie/$', views.BrowseMovieView.as_view(), name='BrowseMovie'),
    url(r'^BrowseActor/$', views.BrowseActorView.as_view(), name='BrowseActor'),
    url(r'^BrowseDirector/$', views.BrowseDirectorView.as_view(), name='BrowseDirector'),
    # Detail
    url(r'^MovieDetail/$', views.MovieDetailView.as_view(), name='MovieDetail'),
    url(r'^ActorDetail/$', views.ActorDetailView.as_view(), name='ActorDetail'),
    url(r'^DirectorDetail/$', views.DirectorDetailView.as_view(), name='DirectorDetail'),
    # Add
    url(r'^AddMovie/$', views.AddMovieView.as_view(), name='AddMovie'),
    url(r'^AddActorDirector/$', views.AddActorDirectorView.as_view(), name='AddActorDirector'),
    url(r'^AddActorMovie/$', views.AddActorToMovieView.as_view(), name='AddActorMovie'),
    url(r'^AddDirectorMovie/$', views.AddDirectorToMovieView.as_view(), name='AddDirectorMovie'),
    # Review
    url(r'^ViewReview/$', views.ViewReviewView.as_view(), name='ViewReview'),
    url(r'^WriteReview/$', views.WriteReviewView.as_view(), name='WriteReview'),
]