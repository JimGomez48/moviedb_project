"""
Context processors run on every request and are merged into every
template's context by ``render()``. This adds the navbar and search form.
"""

from django.urls import NoReverseMatch, reverse

from moviedb import forms
from moviedb.navbar import NAVBAR


class NavElement:
    DROPDOWN = "dropdown"
    ITEM = "item"

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


def _get_navbar_data():
    nav_items = []
    for entry in NAVBAR:
        if entry["type"] == NavElement.DROPDOWN:
            dropdown = NavElement(type=NavElement.DROPDOWN)
            dropdown.text = entry["text"]
            for item in entry["items"]:
                nav_item = NavElement(type=NavElement.ITEM)
                nav_item.text = item["text"]
                try:
                    nav_item.url = reverse(item["viewname"])
                except NoReverseMatch:
                    nav_item.url = "#"
                dropdown.add_child(nav_item)
            nav_items.append(dropdown)
        elif entry["type"] == NavElement.ITEM:
            nav_item = NavElement(type=NavElement.ITEM)
            nav_item.text = entry["text"]
            nav_item.url = reverse(entry["viewname"])
            nav_items.append(nav_item)
    return nav_items


def navbar(request):
    return {
        "title": "MovieDB",
        "nav_items": _get_navbar_data(),
        "search_form": forms.NavBarSearchForm(),
    }
