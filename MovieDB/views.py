import os
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
import xml.etree.cElementTree as ET


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class BaseView(TemplateView):
    class NavElement(object):
        DROPDOWN = 'dropdown'
        ITEM = 'item'
        def __init__(self, type):
            self.type = type
            self.children = None
            self.text = None
            self.url = None

        def add_child(self, child):
            if child:
                if not self.children:
                    self.children = []
                self.children.append(child)

    def get_context_data(self, **kwargs):
        nav_items = self.__get_navbar_elements()
        home_url = reverse('index')
        context = {
            'title': 'MovieDB',
            'home_url': home_url,
            'nav_items': nav_items,
        }
        return context

    def __get_navbar_elements(self):
        # parse navbar.xml to get the navbar information
        navbar = []
        tree = ET.parse(PROJECT_ROOT + '/data/navbar.xml')
        root = tree.getroot()
        for element in root:
            if element.tag == 'dropdown':
                dropdown = self.NavElement(type=self.NavElement.DROPDOWN)
                dropdown.text = element.attrib['name']
                for sub_element in element:
                    nav_item = self.NavElement(type=self.NavElement.ITEM)
                    nav_item.text = sub_element.find('text').text
                    try:
                        nav_item.url = reverse(str(sub_element.find('viewname').text))
                    except NoReverseMatch:
                        nav_item.url = ''
                    dropdown.add_child(nav_item)
                navbar.append(dropdown)
            elif element.tag == 'item':
                nav_item = self.NavElement(type=self.NavElement.ITEM)
                nav_item.text = element.find('text').text
                nav_item.url = reverse(str(element.find('viewname').text))
                navbar.append(nav_item)
        return navbar


class IndexView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['page_header'] = 'MovieDB Landing Page'
        return render(request, 'index.html', context)


class SearchResultsView(BaseView):
    def get(self, request, *args, **kwargs):
        context = super(SearchResultsView, self).get_context_data()
        context['page_header'] = 'Search Results'
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
