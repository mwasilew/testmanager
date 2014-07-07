# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testplanner', '0005_auto_20140702_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='testplan',
            name='automated_build_url',
            field=models.ForeignKey(blank=True, to='testrunner.JenkinsJob', null=True),
            preserve_default=True,
        ),
    ]
