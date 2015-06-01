from django.core.urlresolvers import reverse, NoReverseMatch
import xml.etree.cElementTree as ET
import os

from moviedb_project.settings import BASE_DIR
from MovieDB import models


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


def get_navbar_data():
    # parse navbar.xml to get the navbar information
    navbar = []
    path = os.path.join(BASE_DIR, 'MovieDB/static/data/navbar.xml')
    tree = ET.parse(path)
    root = tree.getroot()
    for element in root:
        if element.tag == 'dropdown':
            dropdown = NavElement(type=NavElement.DROPDOWN)
            dropdown.text = element.attrib['name']
            for sub_element in element:
                nav_item = NavElement(type=NavElement.ITEM)
                nav_item.text = sub_element.find('text').text
                try:
                    nav_item.url = reverse(
                        str(sub_element.find('viewname').text))
                except NoReverseMatch:
                    nav_item.url = ''
                dropdown.add_child(nav_item)
            navbar.append(dropdown)
        elif element.tag == 'item':
            nav_item = NavElement(type=NavElement.ITEM)
            nav_item.text = element.find('text').text
            nav_item.url = reverse(str(element.find('viewname').text))
            navbar.append(nav_item)
    return navbar


def get_movie_details_full(movie_id):
    manager = models.Movie.objects
    movie_details = manager.get_movie_details_full(movie_id)
    return movie_details