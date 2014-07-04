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

import re
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class JenkinsService(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.url)


class JenkinsJob(models.Model):
    name = models.CharField(max_length=128)
    service = models.ForeignKey(JenkinsService)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jenkins_job_view', args=[str(self.name)])

    def get_umbrella_builds(self):
        return self.builds.filter(is_umbrella=True).order_by("-timestamp")

    def get_last_build(self):
        last_umbrella_build = self.builds.filter(is_umbrella=True).order_by("-timestamp")
        if last_umbrella_build:
            return last_umbrella_build[0]
        last_build = self.builds.all().order_by("-timestamp")
        if last_build:
            return last_build[0]
        return None

    def is_last_test_result_green(self):
        last_build = self.get_last_build()
        if last_build:
            if not last_build.is_umbrella:
                for lavajob in last_build.lavajob_set.all():
                    if lavajob.has_results_missing():
                        return False
                    for lavajobresult in lavajob.lavajobresult_set.all():
                        result_count = lavajobresult.get_resultset_count_by_status()
                        if result_count and 'fail' in result_count.keys():
                            return False
                    #for key, value in lavajob.lavajobresult.get_resultset_count_by_status():
                    #    # todo: move status name to settings
                    #    if key == 'fail':
                    #        return False
            else:
                if not self.builds.filter(is_umbrella=False, number=last_build.number):
                    # Jenkins API returnet rubbish
                    return False
                for build in self.builds.filter(is_umbrella=False, number=last_build.number):
                    if not build.lavajob_set.all():
                        return False
                    for lavajob in build.lavajob_set.all():
                        if lavajob.has_results_missing():
                            return False
                        for lavajobresult in lavajob.lavajobresult_set.all():
                            result_count = lavajobresult.get_resultset_count_by_status()
                            if result_count and 'fail' in result_count.keys():
                                return False
        return True


class JenkinsBuildStatus(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


class JenkinsBuild(models.Model):

    name = models.CharField(max_length=1024)
    job = models.ForeignKey(JenkinsJob, related_name="builds")
    umbrella_build = models.ForeignKey("self", blank=True, null=True)
    number = models.IntegerField()
    status = models.ForeignKey(JenkinsBuildStatus)
    is_umbrella = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jenkins_build_view', args=[str(self.job.name), str(self.number)])

    def get_hwpack_name(self):
        if self.is_umbrella:
            return None
        device_regexp = re.compile(ur'%s\s\xbb\s(?P<device_name>\w+)' % (self.job.name), re.UNICODE)
        hwpack_name_search = device_regexp.search(self.name)
        if hwpack_name_search:
            return hwpack_name_search.group('device_name')
        return None


class LavaJobStatus(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


class LavaJob(models.Model):
    jenkins_build = models.ForeignKey(JenkinsBuild)
    number = models.IntegerField()
    status = models.ForeignKey(LavaJobStatus)
    test_definitions = models.ManyToManyField('testplanner.TestDefinition')
    device_type = models.ForeignKey('testplanner.Device')
    submit_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s - LAVA %s" % (self.jenkins_build.job.name, self.number)

    def get_definitions_results(self):
        result_list = []
        for testdef in self.test_definitions.all():
            resultset = LavaJobResult.objects.filter(lava_job = self, test_definition = testdef)
            if resultset:
                result_list.append((testdef, resultset[0]))
            else:
                result_list.append((testdef, None))
        return result_list

    # TODO: move to helpers to be defined during import time, include field for failed tests
    def has_results_missing(self):
        for testdef in self.test_definitions.all():
            resultset = LavaJobResult.objects.filter(lava_job = self, test_definition = testdef)
            if not resultset:
                return True
        return False

    def get_absolute_url(self):
        return reverse(
            'lava_job_view',
            args=[str(self.jenkins_build.job.name),
                  str(self.jenkins_build.number),
                  str(self.number)]
        )


class LavaJobResultStatus(models.Model):
    name = models.CharField(max_length=8)

    def __unicode__(self):
        return self.name


class LavaJobResult(models.Model):
    lava_job = models.ForeignKey(LavaJob)
    test_definition = models.ForeignKey('testplanner.TestDefinition')
    test_revision = models.ForeignKey('testplanner.TestDefinitionRevision', blank=True, null=True)

    def __unicode__(self):
        return "%s result for %s" % (self.lava_job.__unicode__(), self.test_definition.__unicode__())

    def get_resultset_total(self):
        return self.lavajobtestresult_set.count()

    def get_resultset_count_by_status(self):
        status_count = {}
        # TODO: fix this, use aggregate to collect the numbers
        for testresult in self.lavajobtestresult_set.all():
            if testresult.status.name in status_count:
                status_count[testresult.status.name] += 1
            else:
                status_count[testresult.status.name] = 1
        return status_count


class LavaJobTestResultUnit(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class LavaJobTestResult(models.Model):
    test_case_id = models.CharField(max_length=1024)
    lava_job_result = models.ForeignKey(LavaJobResult)
    status = models.ForeignKey(LavaJobResultStatus, blank=True, null=True) # there should be default of 'unknown'
    is_measurement = models.BooleanField(default=False)
    unit = models.ForeignKey(LavaJobTestResultUnit, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.test_case_id



class Bug(models.Model):

    BUGZILLA = "bugzilla"
    JIRA = "jira"
    LAUNCHPAD = "launchpad"

    alias = models.CharField(max_length=32)
    tracker = models.CharField(max_length=16, choices=[(a,a) for a in settings.TRACKERS.keys()])

    class Meta:
        unique_together = ("alias", "tracker")

    def __init__(self, *args, **kwargs):
        super(Bug, self).__init__(*args, **kwargs)
        self._data = {}

    def get_bug(self):
        if not self._data and self.id:
            kwargs = settings.TRACKERS[self.tracker]
            kwargs.pop("type")
            self._data = getattr(self, "_get_%_bug" % self.kind)(**kwargs)
        return self._data

    def _get_bugzilla_bug(self, url, username=None, password=None):
        import requests
        from lxml import etree
        from lxml.etree import fromstring

        if username and password:
            response = requests.get(
                "%sshow_bug.cgi?id=%s&ctype=xml" % (url, self.alias),
                auth=('user', 'pass'))
        else:
            response = requests.get(
                "%sshow_bug.cgi?id=%s&ctype=xml" % (url, self.alias))
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        h = fromstring(response.text.encode('utf-8'), parser=parser)
        short_desc = h.find(".//short_desc")
        bug_status = h.find(".//bug_status")
        bug_severity= h.find(".//bug_severity")

        return {
            'id': self.alias,
            'description': short_desc.text,
            'weblink': "%sshow_bug.cgi?id=%s" % url,
            'severity': bug_severity.text,
            'status': bug_status.text
        }

    def _get_jira_bug(self, url, username=None, password=None):
        from jira.client import JIRA
        options={'server': url, 'verify': False}
        if username and password:
            jira = JIRA(options=options, basic_auth=(username, password))
        else:
            jira = JIRA(options=options)
        jira_bug = jira.issue(self.alias)
        jira_bug_weblink = "%sbrowse/%s" % (url, self.alias)
        return {'alias': self.alias,
                'description': jira_bug.fields.summary,
                'weblink': jira_bug_weblink,
                'severity': jira_bug.fields.priority,
                'status': jira_bug.fields.status}

    def get_launchpad_bug(self, cache_dir):
        from launchpadlib.launchpad import Launchpad

        lp = Launchpad.login_anonymously(
            'qa-reports.linaro.org',
            'production',
            cache_dir,
            version='devel'
        )
        lp_bug = lp.bugs[int(self.alias)]
        lp_severity = ''
        lp_status = ''
        for task in lp_bug.bug_tasks:
            lp_severity += "%s: %s | " % (task.bug_target_display_name, task.importance)
            lp_status += "%s: %s | " % (task.bug_target_display_name, task.status)

        return {
            'alias': self.alias,
            'description': lp_bug.title,
            'weblink': lp_bug.web_link,
            'severity': lp_severity,
            'status': lp_status
        }

