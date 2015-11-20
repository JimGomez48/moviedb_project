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


def load_seed_data_sql():
    print 'Loading seed data...'
    sql = open(os.path.join(BASE_DIR, os.path.normpath('MovieDB/sql/scripts/load_csv.sql')), 'r').read()
    return sql


class Migration(migrations.Migration):
    dependencies = [
        ('MovieDB', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(create_stored_procedures()),
        migrations.RunSQL(load_seed_data_sql()),
    ]
