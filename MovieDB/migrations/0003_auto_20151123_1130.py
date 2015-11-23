# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieDB', '0002_sprocs_seeds'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='cast',
            field=models.ManyToManyField(to='MovieDB.Actor', through='MovieDB.MovieActor'),
        ),
        migrations.AddField(
            model_name='movie',
            name='companies',
            field=models.ManyToManyField(to='MovieDB.Company', through='MovieDB.MovieCompany'),
        ),
        migrations.AddField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(to='MovieDB.Director', through='MovieDB.MovieDirector'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='MovieDB.Genre', through='MovieDB.MovieGenre'),
        ),
    ]
