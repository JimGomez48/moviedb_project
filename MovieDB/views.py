import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
import xml.etree.ElementTree as ET


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class BaseView(TemplateView):
    class NavItem(object):
        def __init__(self, text, url):
            self.text = text
            self.url = url

    def get_context_data(self, **kwargs):
        nav_items = self.__get_navbar_items()
        home_url = reverse('index')
        context = {
            'title': 'MovieDB',
            'home_url': home_url,
            'nav_items': nav_items,
        }
        return context

    def __get_navbar_items(self):
        # parse navbar.xml to get the navbar information
        items = []
        tree = ET.parse(PROJECT_ROOT + '/data/navbar.xml')
        root = tree.getroot()
        for item in root:
            text = item.find('text').text
            url = reverse(str(item.find('viewname').text))
            items.append(self.NavItem(text, url))
        return items


class IndexView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['page_header'] = 'MovieDB Landing Page'
        return render(request, 'index.html', context)


class BrowseMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(BrowseMovieView, self).get_context_data()
        context['page_header'] = 'Browse Movies'
        return render(request, 'browse.html', context)


class BrowseActorView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(BrowseActorView, self).get_context_data()
        context['page_header'] = 'Browse Actors'
        return render(request, 'browse.html', context)


class AddMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddMovieView, self).get_context_data()
        context['page_header'] = 'Add Movies'
        return render(request, 'browse.html', context)


class AddActorDirectorView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorDirectorView, self).get_context_data()
        context['page_header'] = 'Add Actors and Directors'
        return render(request, 'browse.html', context)


class AddActorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddActorToMovieView, self).get_context_data()
        context['page_header'] = 'Add an Actor to a Movie'
        return render(request, 'browse.html', context)


class AddDirectorToMovieView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(AddDirectorToMovieView, self).get_context_data()
        context['page_header'] = 'Add a Director to a Movie'
        return render(request, 'browse.html', context)


class WriteReviewView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(WriteReviewView, self).get_context_data()
        context['page_header'] = 'Write a Movie Review'
        return render(request, 'browse.html', context)
