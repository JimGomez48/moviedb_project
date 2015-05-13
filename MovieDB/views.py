from django.shortcuts import render

def index(request):
    title = 'MovieDB index'
    mlist = ['hello', 'world', 'you', 'suck']
    context = {
        'title': title,
        'mlist': mlist
    }
    return render(request, 'MovieDB/index.html', context)


def browse_movie(request, movie_id=None):
    title = 'Browse Movies'
    context = {
        'title': title
    }
    return render(request, 'MovieDB/index.html', context)


def browse_actor(request, actor_id=None):
    title = 'Browse Actors'
    context = {
        'title': title
    }
    return render(request, 'MovieDB/index.html', context)


def add_movie(request, movie_id=None):
    title = 'Add Movies'
    context = {
        'title': title
    }
    return render(request, 'MovieDB/index.html', context)


def add_actor_director(request, person_id=None):
    title = 'Add Actors/Directors'
    context = {
        'title': title
    }
    return render(request, 'MovieDB/index.html', context)


def add_actor_movie(request, actor_id=None, movie_id=None):
    title = 'Add an actor to a movie'
    context = {
        'title': title
    }
    return render(request, 'MovieDB/index.html', context)


def add_director_movie(request, director_id=None, movie_id=None):
    title = 'Add a director to a movie'
    context = {
        'title': title
    }
    return render(request, 'MovieDB/index.html', context)


def write_review(request, movie_id=None):
    title = 'Add a director to a movie'
    context = {
        'title': title
    }
    return render(request, 'MovieDB/index.html', context)