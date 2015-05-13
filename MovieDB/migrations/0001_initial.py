# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.IntegerField(default=-1, primary_key=True, serialize=False)),
                ('last', models.CharField(default=b'', max_length=20)),
                ('first', models.CharField(default=b'', max_length=20)),
                ('sex', models.CharField(choices=[(b'male', b'male'), (b'male', b'female')], default=b'', max_length=6)),
                ('dob', models.DateField(blank=True, default=datetime.date(1800, 1, 1))),
                ('dod', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.IntegerField(default=-1, primary_key=True, serialize=False)),
                ('last', models.CharField(default=b'', max_length=20)),
                ('first', models.CharField(default=b'', max_length=20)),
                ('dob', models.DateField(blank=True, default=datetime.date(1800, 1, 1))),
                ('dod', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaxMovieID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MaxPersonID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(default=-1, primary_key=True, serialize=False)),
                ('title', models.CharField(default=b'', max_length=100)),
                ('year', models.IntegerField(null=True)),
                ('rating', models.CharField(choices=[(b'NC-17', b'NC-17'), (b'R', b'R'), (b'PG-13', b'PG-13'), (b'PG', b'PG'), (b'G', b'G'), (b'surrendere', b'surrendere')], default=b'', max_length=10)),
                ('company', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieActor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MovieDirector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=b'', max_length=20)),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime(1800, 1, 1, 0, 0))),
                ('mid', models.IntegerField(default=-1)),
                ('rating', models.IntegerField(choices=[(1, b'1-star'), (2, b'2-star'), (3, b'3-star'), (4, b'4-star'), (5, b'5-star')], default=-1)),
                ('comment', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
