# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import datetime
from django.db import migrations, models

from moviedb_project.settings import BASE_DIR
import xml.etree.cElementTree as ET


def load_seed_data(apps, schema_editor):
    print
    print 'loading seed data...'
    SEED_DIR = os.path.join(BASE_DIR, 'MovieDB/sql/seed_data/xml/')

    tree = ET.parse(SEED_DIR + 'actor1.xml')
    root = tree.getroot()
    Actor = apps.get_model('MovieDB', 'Actor')
    actor = Actor()
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

class Migration(migrations.Migration):

    dependencies = [
        ('MovieDB', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_seed_data)
    ]
