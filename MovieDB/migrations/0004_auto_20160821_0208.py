# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieDB', '0003_auto_20151123_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(default=2016, verbose_name=b'Year'),
        ),
    ]
