# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0004_tag_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': [b'-id']},
        ),
    ]
