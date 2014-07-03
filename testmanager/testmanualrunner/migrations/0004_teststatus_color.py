# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0003_auto_20140703_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='teststatus',
            name='color',
            field=models.CharField(default='', max_length=36),
            preserve_default=False,
        ),
    ]
