# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0005_auto_20140709_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='jenkinsbuild',
            name='tags',
            field=models.ManyToManyField(to=b'testrunner.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='jenkinsbuild',
            name='tag',
        ),
    ]
