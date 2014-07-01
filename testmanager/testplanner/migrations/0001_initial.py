# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testrunner', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Maintainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('test_id', models.CharField(max_length=128)),
                ('test_file_name', models.CharField(max_length=256, blank=True)),
                ('description', models.TextField()),
                ('expected', models.TextField(null=True, blank=True)),
                ('default_timeout', models.IntegerField(default=3600)),
                ('default_parameters', jsonfield.fields.JSONField(blank=True)),
                ('is_automated', models.BooleanField(default=True)),
                ('device', models.ManyToManyField(to='testplanner.Device')),
                ('maintainer', models.ManyToManyField(to='testplanner.Maintainer', null=True, blank=True)),
                ('os', models.ManyToManyField(to='testplanner.OS')),
                ('scope', models.ManyToManyField(to='testplanner.Scope')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestDefinitionRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revision', models.CharField(max_length=40)),
                ('test_definition', models.ManyToManyField(to='testplanner.TestDefinition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('external_url', models.URLField(null=True, blank=True)),
                ('default_timeout', models.IntegerField(default=3600)),
                ('automated_build_url', models.ForeignKey(to='testrunner.JenkinsJob', blank=True)),
                ('device', models.ForeignKey(to='testplanner.Device')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestPlanTestDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequence_number', models.PositiveIntegerField()),
                ('parameters', jsonfield.fields.JSONField(blank=True)),
                ('timeout', models.IntegerField()),
                ('test_definition', models.ForeignKey(to='testplanner.TestDefinition')),
                ('test_plan', models.ForeignKey(to='testplanner.TestPlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=200)),
                ('base_view_url', models.URLField()),
                ('description', models.TextField(null=True, blank=True)),
                ('is_cloned', models.BooleanField(default=False)),
                ('local_dir', models.CharField(max_length=1024, null=True, blank=True)),
                ('head_revision', models.CharField(max_length=40, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='testdefinition',
            name='repository',
            field=models.ForeignKey(to='testplanner.TestRepository', blank=True),
            preserve_default=True,
        ),
    ]
