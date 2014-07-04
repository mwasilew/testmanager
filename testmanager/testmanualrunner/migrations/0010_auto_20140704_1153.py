# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0009_auto_20140704_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrunresult',
            name='status',
            field=models.ForeignKey(blank=True, to='testmanualrunner.TestStatus', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='testrunresult',
            unique_together=set([(b'test_run', b'test_definition')]),
        ),
    ]
