# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import migrations
from moviedb_project.settings import BASE_DIR


def create_stored_procedures():
    print 'Creating stored procs...'
    PATH = os.path.join(BASE_DIR, os.path.normpath('MovieDB/sql/sprocs/'))
    sql = ''
    for file in os.listdir(PATH):
        with open(os.path.join(PATH, file), 'r') as sproc:
            sql += sproc.read()
    return sql


def load_static_tables(apps, schema_editor):
    # load mpaa_ratings
    MpaaRating = apps.get_model('MovieDB', 'MpaaRating')
    MpaaRating.objects.bulk_create([
        MpaaRating(value='G'),
        MpaaRating(value='PG'),
        MpaaRating(value='PG-13'),
        MpaaRating(value='R'),
        MpaaRating(value='NC-17'),
        MpaaRating(value='surrendered'),
    ])
    # load genres
    Genre = apps.get_model('MovieDB', 'Genre')
    Genre.objects.bulk_create([
        Genre(value='Action'),
        Genre(value='Adult'),
        Genre(value='Adventure'),
        Genre(value='Animation'),
        Genre(value='Crime'),
        Genre(value='Comedy'),
        Genre(value='Documentary'),
        Genre(value='Drama'),
        Genre(value='Family'),
        Genre(value='Fantasy'),
        Genre(value='Horror'),
        Genre(value='Musical'),
        Genre(value='Mystery'),
        Genre(value='Romance'),
        Genre(value='Sci-Fi'),
        Genre(value='Short'),
        Genre(value='Thriller'),
        Genre(value='War'),
        Genre(value='Western'),
    ])


def load_seed_data_sql():
    print 'Loading seed data...'
    sql = open(os.path.join(BASE_DIR, os.path.normpath('MovieDB/sql/scripts/load_csv.sql')), 'r').read()
    return sql


def load_seed_reviews(apps, schema_editor):
    Review = apps.get_model('MovieDB', 'Review')
    Movie = apps.get_model('MovieDB', 'Movie')
    Review.objects.bulk_create([
        Review(time=u'2015-11-23 05:35:35', user_name=u'Jim',
               movie=Movie.objects.get(id=253), rating=5, comment=u'Great!'),
        Review(time=u'2015-11-23 05:35:35', user_name=u'James',
               movie=Movie.objects.get(id=253), rating=2, comment=u'Ehh...'),
        Review(time=u'2015-11-23 05:35:35', user_name=u'Jimbo',
               movie=Movie.objects.get(id=253), rating=4,
               comment=u'Pretty good'),
    ])


class Migration(migrations.Migration):
    dependencies = [
        ('MovieDB', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_static_tables),
        migrations.RunSQL(load_seed_data_sql()),
        migrations.RunSQL(create_stored_procedures()),
        migrations.RunPython(load_seed_reviews),
    ]
