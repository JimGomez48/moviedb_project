import os
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from django.db import connection

from moviedb_project.settings import BASE_DIR

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

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
#         self.assertTemplateUsed(self.response, 'base.html')


class TestIndexPage(TestCase):
    response = None

    def setUp(self):
        self.response = self.client.get(reverse('Index'))

    def tearDown(self):
        self.response.close()

    def test_uses_index_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

class TestSprocCreation(TestCase):
    def test_sprocs(self):
        print 'Creating stored procs...'
        PATH = os.path.join(BASE_DIR, os.path.normpath('MovieDB/sql/sprocs/'))
        sql = ''
        for file in os.listdir(PATH):
            with open(os.path.join(PATH, file), 'r') as sproc:
                sql += sproc.read()
        print sql

class TestSprocCall(TestCase):
    def test_sproc_call(self):
        cursor = connection.cursor()
        cursor.callproc('sp_get_movie_details_full')
        return None