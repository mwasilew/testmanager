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
                ('kind', models.CharField(max_length=16, choices=[(b'Linaro Bugzilla', b'bugzilla'), (b'Launchpad', b'launchpad'), (b'Launchpad', b'jira')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='bug',
            unique_together=set([(b'alias', b'kind')]),
        ),
    ]
