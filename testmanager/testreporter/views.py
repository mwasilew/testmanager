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

from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from testmanager.views import LoginRequiredMixin
from testmanager.testrunner.models import (
    JenkinsBuild,
    LavaJob,
    Tag,
    Bug
)
from testmanager.testrunner.serializers import (
    BuildSerializer,
    TagSerializer,
    LavaJobSerializer,
    BugSerializer
)
from testmanager.testmanualrunner.models import (
    TestRun,
    TestRunResult
)
from testmanager.testmanualrunner.serializers import TestRunSerializer


class Base(LoginRequiredMixin, TemplateView):
    template_name='testreporter/base.html'

class Public(TemplateView):
    template_name='testreporter/public.html'


class Report_View(APIView):

    def get(self, request, tag_id, format=None):

        tag = Tag.objects.get(id=tag_id)
        builds = JenkinsBuild.objects.filter(tags=tag)
        lava_jobs = LavaJob.objects.filter(jenkins_build__in=builds)
        testruns = TestRun.objects.filter(build__in=builds)

        return Response({
            "builds": BuildSerializer(builds).data,
            "tag": TagSerializer(tag).data,
            "lava_jobs": LavaJobSerializer(lava_jobs).data,
            "testruns": TestRunSerializer(testruns).data,
        })


class Report_Bugs_View(APIView):

    def get(self, request, tag_id, format=None):

        tag = Tag.objects.get(id=tag_id)
        builds = JenkinsBuild.objects.filter(tags=tag)
        lava_jobs = LavaJob.objects.filter(jenkins_build__in=builds)
        testruns = TestRun.objects.filter(build__in=builds)
        testrun_results = TestRunResult.objects.filter(test_run__in=testruns)
        lava_job_bugs = Bug.objects.filter(lavajob__in=lava_jobs)
        testruns_bugs = Bug.objects.filter(testrunresult__in=testrun_results)

        return Response({
            "bugs": BugSerializer(lava_job_bugs | testruns_bugs).data,
        })
