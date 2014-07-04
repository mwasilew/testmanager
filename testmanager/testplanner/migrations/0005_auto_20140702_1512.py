# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testplanner', '0004_auto_20140701_1843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testplan',
            options={'ordering': [b'-id']},
        ),
        migrations.AlterField(
            model_name='testdefinition',
            name='default_parameters',
            field=jsonfield.fields.JSONField(default={}, blank=True),
        ),
        migrations.AlterField(
            model_name='testplantestdefinition',
            name='parameters',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]
