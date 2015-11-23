# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last', models.CharField(max_length=50, verbose_name=b'Last Name')),
                ('first', models.CharField(max_length=50, verbose_name=b'First Name')),
                ('sex', models.CharField(max_length=6, verbose_name=b'Sex', choices=[(b'male', b'Male'), (b'female', b'Female')])),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
                ('dod', models.DateField(default=None, null=True, verbose_name=b'Date of Death')),
            ],
            options={
                'ordering': ['last', 'first'],
                'db_table': 'actors',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Company Name')),
            ],
            options={
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last', models.CharField(max_length=20, verbose_name=b'Last Name')),
                ('first', models.CharField(max_length=20, verbose_name=b'First Name')),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
                ('dod', models.DateField(default=None, null=True, verbose_name=b'Date of Death')),
            ],
            options={
                'ordering': ['last', 'first'],
                'db_table': 'directors',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(default=b'Drama', max_length=20, verbose_name=b'Genre Value', choices=[(b'Action', b'Action'), (b'Adult', b'Adult'), (b'Adventure', b'Adventure'), (b'Animation', b'Animation'), (b'Crime', b'Crime'), (b'Comedy', b'Comedy'), (b'Documentary', b'Documentary'), (b'Drama', b'Drama'), (b'Family', b'Family'), (b'Fantasy', b'Fantasy'), (b'Horror', b'Horror'), (b'Musical', b'Musical'), (b'Mystery', b'Mystery'), (b'Romance', b'Romance'), (b'Sci-Fi', b'Sci-Fi'), (b'Short', b'Short'), (b'Thriller', b'Thriller'), (b'War', b'War'), (b'Western', b'Western')])),
            ],
            options={
                'db_table': 'genres',
            },
        ),
        migrations.CreateModel(
            name='MpaaRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=20, verbose_name=b'Mpaa Rating Value', choices=[(b'NC-17', b'NC-17'), (b'R', b'R'), (b'PG-13', b'PG-13'), (b'PG', b'PG'), (b'G', b'G'), (b'surrendered', b'Not Rated')])),
            ],
            options={
                'db_table': 'mpaa_ratings',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name=b'Movie Title', max_length=100, unique_for_year=b'year')),
                ('year', models.IntegerField(default=2015, verbose_name=b'Year')),
                ('mpaa_rating', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Mpaa Rating', to='MovieDB.MpaaRating')),
            ],
            options={
                'ordering': ['title', 'year'],
                'db_table': 'movies',
            },
        ),
        migrations.CreateModel(
            name='MovieActor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actor', models.ForeignKey(verbose_name=b'Actor', to='MovieDB.Actor')),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
            ],
            options={
                'db_table': 'movie_actors',
            },
        ),
        migrations.CreateModel(
            name='MovieActorRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=50, verbose_name=b'Role')),
                ('movie_actor', models.ForeignKey(to='MovieDB.MovieActor')),
            ],
            options={
                'db_table': 'movie_actor_roles',
            },
        ),
        migrations.CreateModel(
            name='MovieCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(verbose_name=b'Company', to='MovieDB.Company')),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
            ],
            options={
                'db_table': 'movie_companies',
            },
        ),
        migrations.CreateModel(
            name='MovieDirector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('director', models.ForeignKey(verbose_name=b'Director', to='MovieDB.Director')),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
            ],
            options={
                'db_table': 'movie_directors',
            },
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Genre')),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
            ],
            options={
                'db_table': 'movie_genres',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True, verbose_name=b'Time')),
                ('user_name', models.CharField(max_length=20, verbose_name=b'User Name')),
                ('rating', models.IntegerField(default=5, verbose_name=b'User Rating', choices=[(1, b'1-star'), (2, b'2-star'), (3, b'3-star'), (4, b'4-star'), (5, b'5-star')])),
                ('comment', models.TextField(default=b'', max_length=2000, blank=True)),
                ('movie', models.ForeignKey(verbose_name=b'Movie', to='MovieDB.Movie')),
            ],
            options={
                'ordering': ['-time'],
                'db_table': 'reviews',
            },
        ),
    ]
