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
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('last', models.CharField(max_length=50, verbose_name=b'Last Name')),
                ('first', models.CharField(max_length=50, verbose_name=b'First Name')),
                ('sex', models.CharField(max_length=6, verbose_name=b'Sex', choices=[(b'male', b'Male'), (b'female', b'Female')])),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
                ('dod', models.DateField(default=None, null=True, verbose_name=b'Date of Death')),
            ],
            options={
                'ordering': ['last', 'first'],
                'db_table': 'Actors',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('last', models.CharField(max_length=20, verbose_name=b'Last Name')),
                ('first', models.CharField(max_length=20, verbose_name=b'First Name')),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
                ('dod', models.DateField(default=None, null=True, verbose_name=b'Date of Death')),
            ],
            options={
                'ordering': ['last', 'first'],
                'db_table': 'Directors',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('title', models.CharField(verbose_name=b'Movie Title', max_length=100, unique_for_year=b'year')),
                ('year', models.IntegerField(default=2015, verbose_name=b'Year')),
                ('rating', models.CharField(max_length=10, verbose_name=b'MPAA Rating', choices=[(b'NC-17', b'NC-17'), (b'R', b'R'), (b'PG-13', b'PG-13'), (b'PG', b'PG'), (b'G', b'G'), (b'surrendere', b'Not Rated')])),
                ('company', models.CharField(max_length=50, verbose_name=b'Production Company')),
            ],
            options={
                'ordering': ['title', 'year'],
                'db_table': 'Movies',
            },
        ),
        migrations.CreateModel(
            name='MovieActor',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
                ('actor', models.ForeignKey(verbose_name=b'Actor', to='MovieDB.Actor')),
                ('role', models.CharField(max_length=50, verbose_name=b'Role')),
            ],
            options={
                'db_table': 'MovieActors',
            },
        ),
        migrations.CreateModel(
            name='MovieDirector',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
                ('director', models.ForeignKey(verbose_name=b'Director', to='MovieDB.Director')),
            ],
            options={
                'db_table': 'MovieDirectors',
            },
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
                ('genre', models.CharField(default=b'Drama', max_length=20, verbose_name=b'Genre', choices=[(b'Action', b'Action'), (b'Adult', b'Adult'), (b'Adventure', b'Adventure'), (b'Animation', b'Animation'), (b'Crime', b'Crime'), (b'Comedy', b'Comedy'), (b'Documentary', b'Documentary'), (b'Drama', b'Drama'), (b'Family', b'Family'), (b'Fantasy', b'Fantasy'), (b'Horror', b'Horror'), (b'Musical', b'Musical'), (b'Mystery', b'Mystery'), (b'Romance', b'Romance'), (b'Sci-Fi', b'Sci-Fi'), (b'Short', b'Short'), (b'Thriller', b'Thriller'), (b'War', b'War'), (b'Western', b'Western')])),
            ],
            options={
                'db_table': 'MovieGenres',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True, verbose_name=b'Time')),
                ('user_name', models.CharField(max_length=20, verbose_name=b'User Name')),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
                ('rating', models.IntegerField(default=5, verbose_name=b'User Rating', choices=[(1, b'1-star'), (2, b'2-star'), (3, b'3-star'), (4, b'4-star'), (5, b'5-star')])),
                ('comment', models.TextField(default=b'', max_length=2000, blank=True)),
            ],
            options={
                'ordering': ['-time'],
                'db_table': 'Reviews',
            },
        ),
    ]
