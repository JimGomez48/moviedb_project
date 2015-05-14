from django.conf.urls import url

import views

urlpatterns = [
    url(r'^Base/$', views.BaseView.as_view(), name='base'),
    url(r'^$', views.index, name='index'),
    url(r'^BrowseMovie/$', views.browse_movie, name='BrowseMovie'),
    url(r'^BrowseActor/$', views.browse_actor, name='BrowseActor'),
    url(r'^AddMovie/$', views.add_movie, name='AddMovie'),
    url(r'^AddActorDirector/$', views.add_actor_director, name='AddActorDirector'),
    url(r'^AddActorMovie/$', views.add_actor_movie, name='AddActorMovie'),
    url(r'^AddDirectorMovie/$', views.add_director_movie, name='AddDirectorMovie'),
    url(r'^WriteReview/$', views.write_review, name='WriteReview'),
]