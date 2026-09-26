from django.urls import path

from moviedb import views

urlpatterns = [
    # Base
    path("", views.IndexView.as_view(), name="Index"),
    path("SearchResults/", views.SearchResultsView.as_view(), name="SearchResults"),
    path(
        "SearchResults/<str:search_term>/",
        views.SearchResultsView.as_view(),
        name="SearchResults",
    ),
    # Browse Movie
    path("BrowseMovie/", views.BrowseMovieView.as_view(), name="BrowseMovie"),
    path(
        "BrowseMovie/search_term=<str:search_term>/",
        views.BrowseMovieView.as_view(),
        name="BrowseMovie",
    ),
    path(
        "BrowseMovie/page=<int:page_num>/",
        views.BrowseMovieView.as_view(),
        name="BrowseMovie",
    ),
    path(
        "BrowseMovie/search_term=<str:search_term>/page=<int:page_num>/",
        views.BrowseMovieView.as_view(),
        name="BrowseMovie",
    ),
    # Browse Actor
    path("BrowseActor/", views.BrowseActorView.as_view(), name="BrowseActor"),
    path(
        "BrowseActor/search_term=<str:search_term>/",
        views.BrowseActorView.as_view(),
        name="BrowseActor",
    ),
    path(
        "BrowseActor/page=<int:page_num>/",
        views.BrowseActorView.as_view(),
        name="BrowseActor",
    ),
    path(
        "BrowseActor/search_term=<str:search_term>/page=<int:page_num>/",
        views.BrowseActorView.as_view(),
        name="BrowseActor",
    ),
    # Browse Director
    path("BrowseDirector/", views.BrowseDirectorView.as_view(), name="BrowseDirector"),
    path(
        "BrowseDirector/search_term=<str:search_term>/",
        views.BrowseDirectorView.as_view(),
        name="BrowseDirector",
    ),
    path(
        "BrowseDirector/page=<int:page_num>/",
        views.BrowseDirectorView.as_view(),
        name="BrowseDirector",
    ),
    path(
        "BrowseDirector/search_term=<str:search_term>/page=<int:page_num>/",
        views.BrowseDirectorView.as_view(),
        name="BrowseDirector",
    ),
    # Detail
    path("MovieDetail/<int:mid>/", views.MovieDetailView.as_view(), name="MovieDetail"),
    path("ActorDetail/<int:aid>/", views.ActorDetailView.as_view(), name="ActorDetail"),
    path(
        "DirectorDetail/<int:did>/",
        views.DirectorDetailView.as_view(),
        name="DirectorDetail",
    ),
    # Add
    path("AddMovie/", views.AddMovieView.as_view(), name="AddMovie"),
    path(
        "AddActorDirector/",
        views.AddActorDirectorView.as_view(),
        name="AddActorDirector",
    ),
    path("AddActorMovie/", views.AddActorToMovieView.as_view(), name="AddActorMovie"),
    path(
        "AddDirectorMovie/",
        views.AddDirectorToMovieView.as_view(),
        name="AddDirectorMovie",
    ),
    # Review
    path("BrowseReview/", views.BrowseReviewView.as_view(), name="BrowseReview"),
    path("ViewReview/<int:mid>/", views.ViewReviewView.as_view(), name="ViewReview"),
    path("WriteReview/", views.WriteReviewView.as_view(), name="WriteReview"),
    path(
        "WriteReview/<int:mid>/",
        views.WriteReviewView.as_view(),
        name="WriteReview",
    ),
]
