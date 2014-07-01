# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testplanner', '0002_auto_20140701_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplan',
            name='name',
            field=models.CharField(unique=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='testplan',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
