# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0002_auto_20140704_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='tracker',
            field=models.CharField(default=None, max_length=16, choices=[(b'Linaro Bugzilla', b'Linaro Bugzilla'), (b'Launchpad', b'Launchpad'), (b'Linaro Jira', b'Linaro Jira')]),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='bug',
            name='kind',
        ),
        migrations.AlterUniqueTogether(
            name='bug',
            unique_together=set([(b'alias', b'tracker')]),
        ),
    ]
