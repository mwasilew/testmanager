# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testplanner', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='JenkinsBuild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('number', models.IntegerField()),
                ('is_umbrella', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
                ('umbrella_build', models.ForeignKey(blank=True, to='testrunner.JenkinsBuild', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JenkinsBuildStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='jenkinsbuild',
            name='status',
            field=models.ForeignKey(to='testrunner.JenkinsBuildStatus'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='JenkinsJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='jenkinsbuild',
            name='job',
            field=models.ForeignKey(to='testrunner.JenkinsJob'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='JenkinsService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='jenkinsjob',
            name='service',
            field=models.ForeignKey(to='testrunner.JenkinsService'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LavaJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('submit_time', models.DateTimeField(null=True, blank=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('device_type', models.ForeignKey(to='testplanner.Device')),
                ('jenkins_build', models.ForeignKey(to='testrunner.JenkinsBuild')),
                ('test_definitions', models.ManyToManyField(to='testplanner.TestDefinition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LavaJobResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lava_job', models.ForeignKey(to='testrunner.LavaJob')),
                ('test_definition', models.ForeignKey(to='testplanner.TestDefinition')),
                ('test_revision', models.ForeignKey(blank=True, to='testplanner.TestDefinitionRevision', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LavaJobResultStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LavaJobStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lavajob',
            name='status',
            field=models.ForeignKey(to='testrunner.LavaJobStatus'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LavaJobTestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_case_id', models.CharField(max_length=1024)),
                ('is_measurement', models.BooleanField(default=False)),
                ('value', models.FloatField(null=True, blank=True)),
                ('lava_job_result', models.ForeignKey(to='testrunner.LavaJobResult')),
                ('status', models.ForeignKey(blank=True, to='testrunner.LavaJobResultStatus', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LavaJobTestResultUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lavajobtestresult',
            name='unit',
            field=models.ForeignKey(blank=True, to='testrunner.LavaJobTestResultUnit', null=True),
            preserve_default=True,
        ),
    ]
