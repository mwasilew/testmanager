# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=32)),
                ('tracker', models.CharField(max_length=16, choices=[(b'Linaro Bugzilla', b'Linaro Bugzilla'), (b'Launchpad', b'Launchpad'), (b'Linaro Jira', b'Linaro Jira')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='bug',
            unique_together=set([(b'alias', b'tracker')]),
        ),
    ]
