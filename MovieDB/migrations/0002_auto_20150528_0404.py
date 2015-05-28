# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import datetime
from django.db import migrations, models

from moviedb_project.settings import BASE_DIR
import xml.etree.cElementTree as ET

SEED_DIR = os.path.join(BASE_DIR, 'MovieDB/sql/seed_data/xml/')

def seed_actor(apps, schema_editor):
    Actor = apps.get_model('MovieDB', 'Actor')
    actor = Actor()
    tree = ET.parse(SEED_DIR + 'actor1.xml')
    root = tree.getroot()
    for row in root:
        actor.id = row.find('id').text
        actor.last = row.find('last').text
        actor.first = row.find('first').text
        actor.sex= row.find('sex').text
        dob_raw = row.find('dob').text
        actor.dob = datetime.date(
            year=int(dob_raw[:4]),
            month=int(dob_raw[4:6]),
            day=int(dob_raw[6:8])
        )
        dod_raw = row.find('dod').text
        if dod_raw and dod_raw != "\\N":
            actor.dod = datetime.date(
                year=int(dod_raw[:4]),
                month=int(dod_raw[4:6]),
                day=int(dod_raw[6:8])
            )
        else:
            actor.dod = None
        actor.save()
    tree = ET.parse(SEED_DIR + 'actor2.xml')
    root = tree.getroot()
    # Actor = apps.get_model('MovieDB', 'Actor')
    # actor = Actor()
    for row in root:
        actor.id = row.find('id').text
        actor.last = row.find('last').text
        actor.first = row.find('first').text
        actor.sex= row.find('sex').text
        dob_raw = row.find('dob').text
        actor.dob = datetime.date(
            year=int(dob_raw[:4]),
            month=int(dob_raw[4:6]),
            day=int(dob_raw[6:8])
        )
        dod_raw = row.find('dod').text
        if dod_raw and dod_raw != "\\N":
            actor.dod = datetime.date(
                year=int(dod_raw[:4]),
                month=int(dod_raw[4:6]),
                day=int(dod_raw[6:8])
            )
        else:
            actor.dod = None
        actor.save()
    tree = ET.parse(SEED_DIR + 'actor3.xml')
    root = tree.getroot()
    # Actor = apps.get_model('MovieDB', 'Actor')
    # actor = Actor()
    for row in root:
        actor.id = row.find('id').text
        actor.last = row.find('last').text
        actor.first = row.find('first').text
        actor.sex= row.find('sex').text
        dob_raw = row.find('dob').text
        actor.dob = datetime.date(
            year=int(dob_raw[:4]),
            month=int(dob_raw[4:6]),
            day=int(dob_raw[6:8])
        )
        dod_raw = row.find('dod').text
        if dod_raw and dod_raw != "\\N":
            actor.dod = datetime.date(
                year=int(dod_raw[:4]),
                month=int(dod_raw[4:6]),
                day=int(dod_raw[6:8])
            )
        else:
            actor.dod = None
        actor.save()


def seed_director(apps, schema_editor):
    Director = apps.get_model('MovieDB', 'Director')
    director = Director()
    tree = ET.parse(SEED_DIR + 'director.xml')
    root = tree.getroot()
    for row in root:
        director.id = row.find('id').text
        director.last = row.find('last').text
        director.first = row.find('first').text
        dob_raw = row.find('dob').text
        director.dob = datetime.date(
            year=int(dob_raw[:4]),
            month=int(dob_raw[4:6]),
            day=int(dob_raw[6:8])
        )
        dod_raw = row.find('dod').text
        if dod_raw and dod_raw != "\\N":
            director.dod = datetime.date(
                year=int(dod_raw[:4]),
                month=int(dod_raw[4:6]),
                day=int(dod_raw[6:8])
            )
        else:
            director.dod = None
        director.save()


def seed_movie(apps, schema_editor):
    Movie = apps.get_model('MovieDB', 'Movie')
    movie = Movie()
    tree = ET.parse(SEED_DIR + 'movie.xml')
    root = tree.getroot()
    for row in root:
        movie.id = row.find('id').text
        movie.title = row.find('title').text
        movie.year = row.find('year').text
        movie.rating = row.find('rating').text
        movie.company = row.find('company').text
        movie.save()


def seed_movie_actor(apps, schema_editor):
    MovieActor = apps.get_model('MovieDB', 'MovieActor')
    movie_actor = MovieActor()
    tree = ET.parse(SEED_DIR + 'movieactor1.xml')
    root = tree.getroot()
    for row in root:
        movie_actor.role = row.find('role').text
        movie_actor.mid.id = int(row.find('movie_id').text)
        movie_actor.aid.id = int(row.find('actor_id').text)
        movie_actor.save()
    tree = ET.parse(SEED_DIR + 'movieactor2.xml')
    root = tree.getroot()
    for row in root:
        movie_actor.role = row.find('role').text
        movie_actor.mid.id = int(row.find('movie_id'))
        movie_actor.aid.id = int(row.find('actor_id').text)
        movie_actor.save()


def seed_movie_director(apps, schema_editor):
    pass


def seed_movie_genre(apps, schema_editor):
    pass


def seed_max_person_id(apps, schema_editor):
    pass


def seed_max_movie_id(apps, schema_editor):
    pass


def load_seed_data(apps, schema_editor):
    print
    print 'loading seed data...'
    seed_actor(apps, schema_editor)
    seed_director(apps, schema_editor)
    seed_movie(apps, schema_editor)
    seed_movie_actor(apps, schema_editor)
    seed_movie_director(apps, schema_editor)
    seed_movie_genre(apps, schema_editor)
    seed_max_person_id(apps, schema_editor)
    seed_max_movie_id(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('MovieDB', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_seed_data)
    ]
