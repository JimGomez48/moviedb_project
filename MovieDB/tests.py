import os
from django.core.urlresolvers import reverse
from django.test import TestCase


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class TestBasePage(TestCase):
    response = None

    def setUp(self):
        self.response = self.client.get(reverse('base'))

    def tearDown(self):
        self.response.close()

    def test_uses_base_template(self):
        self.assertTemplateUsed(self.response, 'base.html')


class TestIndexPage(TestCase):
    response = None

    def setUp(self):
        self.response = self.client.get(reverse('index'))

    def tearDown(self):
        self.response.close()

    def test_uses_index_template(self):
        self.assertTemplateUsed(self.response, 'index.html')
