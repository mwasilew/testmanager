# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testplanner', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('test_plan', models.ForeignKey(to='testplanner.TestPlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestRunResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('test_definition', models.ForeignKey(to='testplanner.TestDefinition')),
                ('test_run', models.ForeignKey(to='testmanualrunner.TestRun')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
