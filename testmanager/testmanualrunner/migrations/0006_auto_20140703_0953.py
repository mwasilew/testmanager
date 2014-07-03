# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0005_auto_20140703_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrun',
            name='updated_at',
            field=models.DateTimeField(default=datetime.now(), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testrunresult',
            name='updated_at',
            field=models.DateTimeField(default=datetime.now(), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testrun',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='testrunresult',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
