# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('last', models.CharField(max_length=20)),
                ('first', models.CharField(max_length=20)),
                ('sex', models.CharField(max_length=6, choices=[(b'male', b'male'), (b'female', b'female')])),
                ('dob', models.DateField()),
                ('dod', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('last', models.CharField(max_length=20)),
                ('first', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('dod', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaxMovieID',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaxPersonID',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('year', models.IntegerField(default=b'', blank=True)),
                ('rating', models.CharField(max_length=10, choices=[(b'NC-17', b'NC-17'), (b'R', b'R'), (b'PG-13', b'PG-13'), (b'PG', b'PG'), (b'G', b'G'), (b'surrendere', b'surrendere')])),
                ('company', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MovieActor',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('role', models.CharField(max_length=50)),
                ('aid', models.ForeignKey(to='MovieDB.Actor', db_column=b'aid')),
                ('mid', models.ForeignKey(to='MovieDB.Movie', db_column=b'mid')),
            ],
        ),
        migrations.CreateModel(
            name='MovieDirector',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('did', models.ForeignKey(to='MovieDB.Director', db_column=b'did')),
                ('mid', models.ForeignKey(to='MovieDB.Movie', db_column=b'mid')),
            ],
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('genre', models.CharField(max_length=20, choices=[(b'Action', b'Action'), (b'Adult', b'Adult'), (b'Adventure', b'Adventure'), (b'Animation', b'Animation'), (b'Crime', b'Crime'), (b'Comedy', b'Comedy'), (b'Documentary', b'Documentary'), (b'Drama', b'Drama'), (b'Family', b'Family'), (b'Fantasy', b'Fantasy'), (b'Horror', b'Horror'), (b'Musical', b'Musical'), (b'Mystery', b'Mystery'), (b'Romance', b'Romance'), (b'Sci-Fi', b'Sci-Fi'), (b'Short', b'Short'), (b'Thriller', b'Thriller'), (b'War', b'War'), (b'Western', b'Western')])),
                ('mid', models.ForeignKey(to='MovieDB.Movie', db_column=b'mid')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('user_name', models.CharField(max_length=20)),
                ('rating', models.IntegerField(choices=[(1, b'1-star'), (2, b'2-star'), (3, b'3-star'), (4, b'4-star'), (5, b'5-star')])),
                ('comment', models.CharField(default=b'', max_length=500, blank=True)),
                ('mid', models.ForeignKey(to='MovieDB.Movie', db_column=b'mid')),
            ],
        ),
    ]
