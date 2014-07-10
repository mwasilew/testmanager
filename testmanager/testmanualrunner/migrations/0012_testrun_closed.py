# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0011_testrunresult_bugs'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrun',
            name='closed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
