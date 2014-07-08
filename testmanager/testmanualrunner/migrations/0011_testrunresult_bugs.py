# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0010_auto_20140704_1153'),
        ('testrunner', '0003_auto_20140707_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrunresult',
            name='bugs',
            field=models.ManyToManyField(to=b'testrunner.Bug', blank=True),
            preserve_default=True,
        ),
    ]
