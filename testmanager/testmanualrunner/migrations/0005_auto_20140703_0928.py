# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def default_statuses(apps, schema_editor):
    TestStatus = apps.get_model("testmanualrunner", "TestStatus")
    TestStatus.objects.get_or_create(
        name="pass",
        color="green"
    )
    TestStatus.objects.get_or_create(
        name="fail",
        color="red"
    )
    TestStatus.objects.get_or_create(
        name="skip",
        color="gray"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0004_teststatus_color'),
    ]

    operations = [
        migrations.RunPython(default_statuses),
    ]
