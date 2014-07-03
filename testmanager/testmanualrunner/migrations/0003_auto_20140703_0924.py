# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testmanualrunner', '0002_testrun_build'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=36)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='testrunresult',
            name='status',
            field=models.ForeignKey(default='', to='testmanualrunner.TestStatus'),
            preserve_default=False,
        ),
    ]
