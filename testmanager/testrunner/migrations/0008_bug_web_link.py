# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0007_auto_20140710_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='web_link',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
