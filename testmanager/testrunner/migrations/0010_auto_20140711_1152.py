# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0009_lavajobresult_bugs'),
    ]

    operations = [
        migrations.AddField(
            model_name='lavajob',
            name='bugs',
            field=models.ManyToManyField(to=b'testrunner.Bug', blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='lavajobresult',
            name='bugs',
        ),
    ]
