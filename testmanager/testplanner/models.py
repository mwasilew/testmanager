# Copyright (C) 2014 Linaro Limited
#
# Author: Milosz Wasilewski <milosz.wasilewski@linaro.org>
#
# This file is part of Testmanager.
#
# Testmanager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation
#
# Testmanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Testmanager.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from jsonfield import JSONField


class TestRepository(models.Model):
    """ Represents a git (only?) repository
        that contains yaml files with test definitions
    """
    url = models.CharField(max_length=200)
    base_view_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    is_cloned = models.BooleanField(default=False)
    local_dir = models.CharField(max_length=1024, blank=True, null=True)
    head_revision = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.url


class Maintainer(models.Model):
    email = models.EmailField()

    def __unicode__(self):
        return self.email


class OS(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Scope(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class TestPlan(models.Model):
    """ Represents a set of test definitions
        that are executed on one device type in LAVA.
        Test plan corresponds to single build,
        so different builds will have separate test plans.
    """
    class Meta:
        ordering = ['-id']


    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(blank=True)

    owner = models.ForeignKey(User)
    description = models.TextField()
    external_url = models.URLField(blank=True, null=True)
    default_timeout = models.IntegerField(default=3600)

    device = models.ForeignKey(Device)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(TestPlan, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class TestDefinition(models.Model):
    """ Represents a single YAML file """
    #slug = models.SlugField()
    name = models.CharField(max_length=128, unique=True)
    test_id = models.CharField(max_length=128)
    repository = models.ForeignKey(TestRepository, blank=True)
    test_file_name = models.CharField(max_length=256, blank=True)
    description = models.TextField()
    expected = models.TextField(blank=True, null=True)
    maintainer = models.ManyToManyField(Maintainer, blank=True, null=True)
    os = models.ManyToManyField(OS)
    scope = models.ManyToManyField(Scope)
    device = models.ManyToManyField(Device)
    default_timeout = models.IntegerField(default=3600)
    default_parameters = JSONField(blank=True, default={})
    is_automated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class TestDefinitionRevision(models.Model):
    test_definition = models.ManyToManyField(TestDefinition)
    revision = models.CharField(max_length=40)

    def __unicode__(self):
        return self.revision


class TestPlanTestDefinition(models.Model):
    """
    Represents TestDefinition instance that
    is included in the test plan
    """

    test_definition = models.ForeignKey(TestDefinition)
    test_plan = models.ForeignKey(TestPlan)
    sequence_number = models.PositiveIntegerField(null=True)
    parameters = JSONField(default={})
    timeout = models.IntegerField(null=True)

    def __unicode__(self):
        return "#%s in %s (%s)" % (self.sequence_number, self.test_plan.name, self.test_definition.name)
