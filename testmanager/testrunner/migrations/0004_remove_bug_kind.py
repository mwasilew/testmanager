# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0003_auto_20140704_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bug',
            name='kind',
        ),
    ]
