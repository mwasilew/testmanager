# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0008_teststatus_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrunresult',
            name='status',
            field=models.ForeignKey(to='testmanualrunner.TestStatus', null=True),
        ),
    ]
