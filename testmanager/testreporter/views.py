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

# Create your views here.

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.generic import TemplateView

from testmanager.testrunner.models import JenkinsBuild, LavaJob, LavaJobResult, Tag
from testmanager.testrunner import views as testrunner_views


class BuildSerializer(serializers.ModelSerializer):

    class Meta:
        model = JenkinsBuild


class Base(TemplateView):
    template_name='testreporter/base.html'


class Report_View(APIView):
    def get(self, request, tag_id, format=None):

        tag = Tag.objects.get(id=tag_id)
        builds = JenkinsBuild.objects.filter(tag=tag)
        lava_jobs = LavaJob.objects.filter(jenkins_build__in=builds)
        lava_jobs_results = LavaJobResult.objects\
                                         .filter(lava_job__in=lava_jobs)\
                                         .select_related("test_definition")\
                                         .prefetch_related("lavajobtestresult_set")

        automatic_tests_results = [{
            "name": a.test_definition.name,
            "results": a.get_resultset_count_by_status()} for a in lava_jobs_results
        ]

        return Response({
            "builds": BuildSerializer(builds).data,
            "tag": testrunner_views.TagSerializer(tag).data,
            "lava_jobs": testrunner_views.LavaJobSerializer(lava_jobs).data,
            "lava_results": automatic_tests_results
        })
