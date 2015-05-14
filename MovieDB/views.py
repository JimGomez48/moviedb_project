import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
import xml.etree.ElementTree as ET


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class BaseView(View):
    class NavItem(object):
        def __init__(self, text, tooltip, url):
            self.text = text
            self.tooltip = tooltip
            self.url = url

    def get(self, request):
        nav_items = self.__get_navbar_items()
        context = {
            'nav_items': nav_items
        }
        return render(request, 'base.html', context)
        # return HttpResponse('hello base')

    def __get_navbar_items(self):
        items = []
        tree = ET.parse(PROJECT_ROOT + '/data/navbar.xml')
        root = tree.getroot()
        for item in root:
            text = item.find('text').text
            tooltip = item.find('tooltip').text
            url = reverse(str(item.find('viewname').text))
            items.append(self.NavItem(text, tooltip, url))
        return items


def index(request):
    title = 'MovieDB index'
    mlist = ['hello', 'world', 'you', 'suck']
    context = {
        'title': title,
        'mlist': mlist
    }
    return render(request, 'index.html', context)


def browse_movie(request, movie_id=None):
    title = 'Browse Movies'
    context = {
        'title': title
    }
    return render(request, 'index.html', context)


def browse_actor(request, actor_id=None):
    title = 'Browse Actors'
    context = {
        'title': title
    }
    return render(request, 'index.html', context)


def add_movie(request, movie_id=None):
    title = 'Add Movies'
    context = {
        'title': title
    }
    return render(request, 'index.html', context)


def add_actor_director(request, person_id=None):
    title = 'Add Actors/Directors'
    context = {
        'title': title
    }
    return render(request, 'index.html', context)


def add_actor_movie(request, actor_id=None, movie_id=None):
    title = 'Add an actor to a movie'
    context = {
        'title': title
    }
    return render(request, 'index.html', context)


def add_director_movie(request, director_id=None, movie_id=None):
    title = 'Add a director to a movie'
    context = {
        'title': title
    }
    return render(request, 'index.html', context)


def write_review(request, movie_id=None):
    title = 'Add a director to a movie'
    context = {
        'title': title
    }
    return render(request, 'index.html', context)