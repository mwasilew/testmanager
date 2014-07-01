# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testplanner', '0003_auto_20140701_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplantestdefinition',
            name='sequence_number',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='testplantestdefinition',
            name='timeout',
            field=models.IntegerField(null=True),
        ),
    ]
