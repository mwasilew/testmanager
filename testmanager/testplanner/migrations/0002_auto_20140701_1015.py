# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testplanner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplan',
            name='automated_build_url',
            field=models.ForeignKey(blank=True, to='testrunner.JenkinsJob', null=True),
        ),
    ]
