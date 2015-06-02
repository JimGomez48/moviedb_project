import os
import unittest
from django.db import connection

from moviedb_project.settings import BASE_DIR

class TestMigrations(unittest.TestCase):
    def test_load_seed_data(self):
        print 'Loading seed data...'
        try:
            sql = open(os.path.join(BASE_DIR, os.path.normpath('MovieDB/sql/scripts/load.sql')), 'r').read()
            print sql
        except StandardError as e:
            self.fail(e.message)

    def test_create_sprocs(self):
        print 'Creating stored procs...'
        PATH = os.path.join(BASE_DIR, os.path.normpath('MovieDB/sql/sprocs/'))
        sql = ''
        for file in os.listdir(PATH):
            with open(os.path.join(PATH, file), 'r') as sproc:
                sql += sproc.read()
        print sql


class TestSprocCall(unittest.TestCase):
    @unittest.skip('')
    def test_sproc_call(self):
        proc_name = 'movie_db.sp_get_movie_details_full'
        cursor = connection.cursor()
        cursor.callproc(proc_name, [253])

        # actors
        results = cursor.fetchall()
        print results
        # directors
        cursor.nextset()
        results = cursor.fetchall()
        print results
        # genres
        cursor.nextset()
        results = cursor.fetchall()
        print results
        # reviews
        cursor.nextset()
        results = cursor.fetchall()
        print results
        # avg rating
        cursor.nextset()
        results = cursor.fetchall()
        print results

        return None