# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import migrations, models
from moviedb_project.settings import BASE_DIR

def create_stored_procedures():
    print 'Creating stored procs...'
    PATH = os.path.join(BASE_DIR, os.path.normpath('MovieDB/sql/sprocs/'))
    sql = ''
    for file in os.listdir(PATH):
        with open(os.path.join(PATH, file), 'r') as sproc:
            sql += sproc.read()
    return sql

class Migration(migrations.Migration):

    dependencies = [
        ('MovieDB', '0002_load_seed_data'),
    ]

    operations = [
    ]
