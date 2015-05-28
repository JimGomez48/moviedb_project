# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('last', models.CharField(max_length=20)),
                ('first', models.CharField(max_length=20)),
                ('sex', models.CharField(choices=[(b'male', b'male'), (b'female', b'female')], max_length=6)),
                ('dob', models.DateField()),
                ('dod', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('last', models.CharField(max_length=20)),
                ('first', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('dod', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaxMovieID',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MaxPersonID',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('year', models.IntegerField(blank=True, default=b'')),
                ('rating', models.CharField(choices=[(b'NC-17', b'NC-17'), (b'R', b'R'), (b'PG-13', b'PG-13'), (b'PG', b'PG'), (b'G', b'G'), (b'surrendere', b'surrendere')], max_length=10)),
                ('company', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MovieActor',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=50)),
                ('actor', models.ForeignKey(to='MovieDB.Actor')),
                ('movie', models.ForeignKey(to='MovieDB.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieDirector',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('director', models.ForeignKey(to='MovieDB.Director')),
                ('movie', models.ForeignKey(to='MovieDB.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('genre', models.CharField(choices=[(b'Action', b'Action'), (b'Adult', b'Adult'), (b'Adventure', b'Adventure'), (b'Animation', b'Animation'), (b'Crime', b'Crime'), (b'Comedy', b'Comedy'), (b'Documentary', b'Documentary'), (b'Drama', b'Drama'), (b'Family', b'Family'), (b'Fantasy', b'Fantasy'), (b'Horror', b'Horror'), (b'Musical', b'Musical'), (b'Mystery', b'Mystery'), (b'Romance', b'Romance'), (b'Sci-Fi', b'Sci-Fi'), (b'Short', b'Short'), (b'Thriller', b'Thriller'), (b'War', b'War'), (b'Western', b'Western')], max_length=20)),
                ('movie', models.ForeignKey(to='MovieDB.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
                ('rating', models.IntegerField(choices=[(1, b'1-star'), (2, b'2-star'), (3, b'3-star'), (4, b'4-star'), (5, b'5-star')])),
                ('comment', models.CharField(blank=True, default=b'', max_length=500)),
                ('movie', models.ForeignKey(to='MovieDB.Movie')),
            ],
        ),
    ]
