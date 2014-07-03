# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations



def default_statuses(apps, schema_editor):
    TestStatus = apps.get_model("testmanualrunner", "TestStatus")
    TestStatus.objects.get_or_create(
        name="pass",
        color="green",
        icon="glyphicon-ok"
    )
    TestStatus.objects.get_or_create(
        name="fail",
        color="red",
        icon="glyphicon-remove"
    )
    TestStatus.objects.get_or_create(
        name="skip",
        color="gray",
        icon="glyphicon-flag"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0006_auto_20140703_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='teststatus',
            name='icon',
            field=models.CharField(default='', max_length=36, blank=True),
            preserve_default=False,
        ),
        migrations.RunPython(default_statuses),
    ]
