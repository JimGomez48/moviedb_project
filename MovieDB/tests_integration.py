# import os
# from django.core.urlresolvers import reverse
# from django.test import TestCase
# from django.test import Client
# from django.db import connection
#
# from moviedb_project.settings import BASE_DIR
#
# class TestBasePage(TestCase):
#     response = None
#
#     def setUp(self):
#         self.response = self.client.get(reverse('index'))
#
#     def tearDown(self):
#         self.response.close()
#
#     def test_uses_base_template(self):
#         self.assertTemplateUsed(self.response, 'base_view.html')
#
#
# class TestIndexPage(TestCase):
#     response = None
#
#     def setUp(self):
#         self.response = self.client.get(reverse('Index'))
#
#     def tearDown(self):
#         self.response.close()
#
#     def test_uses_index_template(self):
#         self.assertTemplateUsed(self.response, 'index.html')
