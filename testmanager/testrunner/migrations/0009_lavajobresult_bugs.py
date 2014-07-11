# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0008_bug_web_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='lavajobresult',
            name='bugs',
            field=models.ManyToManyField(to=b'testrunner.Bug', blank=True),
            preserve_default=True,
        ),
    ]
