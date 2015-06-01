from moviedb_project import settings
import os
import unittest
from django.db import connection


class TestSprocCall(unittest.TestCase):
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