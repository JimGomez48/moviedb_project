from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^BrowseMovie/$', views.BrowseMovieView.as_view(), name='BrowseMovie'),
    url(r'^BrowseActor/$', views.BrowseActorView.as_view(), name='BrowseActor'),
    url(r'^AddMovie/$', views.AddMovieView.as_view(), name='AddMovie'),
    url(r'^AddActorDirector/$', views.AddActorDirectorView.as_view(), name='AddActorDirector'),
    url(r'^AddActorMovie/$', views.AddActorToMovieView.as_view(), name='AddActorMovie'),
    url(r'^AddDirectorMovie/$', views.AddDirectorToMovieView.as_view(), name='AddDirectorMovie'),
    url(r'^WriteReview/$', views.WriteReviewView.as_view(), name='WriteReview'),
]