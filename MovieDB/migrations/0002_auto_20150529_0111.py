# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import migrations, models
from moviedb_project.settings import BASE_DIR

def load_seed_data_sql():
    sql_statements = open(os.path.join(BASE_DIR, 'MovieDB/sql/scripts/load.sql'), 'r').read()
    return sql_statements


class Migration(migrations.Migration):

    dependencies = [
        ('MovieDB', '0001_initial'),
    ]

    operations = [
        # migrations.RunSQL(load_seed_data_sql())
    ]
