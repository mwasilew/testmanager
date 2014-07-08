# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0010_auto_20140704_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrunresult',
            name='bugs',
            field=models.ManyToManyField(to=b'testrunner.Bug'),
            preserve_default=True,
        ),
    ]
