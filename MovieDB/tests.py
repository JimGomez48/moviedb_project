import os
from django.core.urlresolvers import reverse
from django.test import TestCase
import xmltodict

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class TestBasePage(TestCase):
    def test_uses_base_template(self):
        response = self.client.get(reverse('base'))
        self.assertTemplateUsed(response, 'base.html')

    def test_uses_correct_css(self):
        pass


class TestIndexPage(TestCase):
    def test_uses_index_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')


class TestBrowseMoviePage(TestCase):
    pass


class TestBrowseActorPage(TestCase):
    pass