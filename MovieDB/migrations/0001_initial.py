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
                ('last', models.CharField(max_length=50, verbose_name='Last Name')),
                ('first', models.CharField(max_length=50, verbose_name='First Name')),
                ('sex', models.CharField(max_length=6, verbose_name='Sex', choices=[('male', 'Male'), ('female', 'Female')])),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('dod', models.DateField(default=None, null=True, verbose_name='Date of Death')),
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
                ('name', models.CharField(max_length=50, verbose_name='Company Name')),
            ],
            options={
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last', models.CharField(max_length=20, verbose_name='Last Name')),
                ('first', models.CharField(max_length=20, verbose_name='First Name')),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('dod', models.DateField(default=None, null=True, verbose_name='Date of Death')),
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
                ('value', models.CharField(default='Drama', max_length=20, verbose_name='Genre Value', choices=[('Action', 'Action'), ('Adult', 'Adult'), ('Adventure', 'Adventure'), ('Animation', 'Animation'), ('Crime', 'Crime'), ('Comedy', 'Comedy'), ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Musical', 'Musical'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Sci-Fi', 'Sci-Fi'), ('Short', 'Short'), ('Thriller', 'Thriller'), ('War', 'War'), ('Western', 'Western')])),
            ],
            options={
                'db_table': 'genres',
            },
        ),
        migrations.CreateModel(
            name='MpaaRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=20, verbose_name='Mpaa Rating Value', choices=[('NC-17', 'NC-17'), ('R', 'R'), ('PG-13', 'PG-13'), ('PG', 'PG'), ('G', 'G'), ('surrendered', 'Not Rated')])),
            ],
            options={
                'db_table': 'mpaa_ratings',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='Movie Title', max_length=100, unique_for_year='year')),
                ('year', models.IntegerField(default=2015, verbose_name='Year')),
                ('mpaa_rating', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Mpaa Rating', to='MovieDB.MpaaRating')),
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
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Actor', to='MovieDB.Actor')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Movie', to='MovieDB.Movie')),
            ],
            options={
                'db_table': 'movie_actors',
            },
        ),
        migrations.CreateModel(
            name='MovieActorRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=50, verbose_name='Role')),
                ('movie_actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MovieDB.MovieActor')),
            ],
            options={
                'db_table': 'movie_actor_roles',
            },
        ),
        migrations.CreateModel(
            name='MovieCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Company', to='MovieDB.Company')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Movie', to='MovieDB.Movie')),
            ],
            options={
                'db_table': 'movie_companies',
            },
        ),
        migrations.CreateModel(
            name='MovieDirector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Director', to='MovieDB.Director')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Movie', to='MovieDB.Movie')),
            ],
            options={
                'db_table': 'movie_directors',
            },
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Movie', to='MovieDB.Genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Movie', to='MovieDB.Movie')),
            ],
            options={
                'db_table': 'movie_genres',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True, verbose_name='Time')),
                ('user_name', models.CharField(max_length=20, verbose_name='User Name')),
                ('rating', models.IntegerField(default=5, verbose_name='User Rating', choices=[(1, '1-star'), (2, '2-star'), (3, '3-star'), (4, '4-star'), (5, '5-star')])),
                ('comment', models.TextField(default='', max_length=2000, blank=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='Movie', to='MovieDB.Movie')),
            ],
            options={
                'ordering': ['-time'],
                'db_table': 'reviews',
            },
        ),
    ]
