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

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from testmanager.testrunner.models import (
    JenkinsJob,
    JenkinsBuild,
    LavaJob,
    LavaJobTestResult,
    LavaJobResult,
    Tag,
    Bug
)
from testmanager.testrunner.forms import ResultComparisonForm
from testmanager.testmanualrunner.models import TestStatus


@login_required
def index(request):
    jenkins_jobs = JenkinsJob.objects.all()
    template = loader.get_template('testrunner/index.html')
    context = RequestContext(request, {
        'jenkins_jobs': jenkins_jobs,
    })
    return HttpResponse(template.render(context))

@login_required
def jenkins_job_view(request, job_name):
    jenkins_job = get_object_or_404(JenkinsJob, name=job_name)
    jenkins_builds = jenkins_job.builds.filter(is_umbrella=False).order_by("-timestamp")[:10]
    template = loader.get_template('testrunner/jenkins_job_view.html')
    context = RequestContext(request, {
        'jenkins_job': jenkins_job,
        'jenkins_builds': jenkins_builds
    })
    return HttpResponse(template.render(context))


@login_required
def jenkins_build_view(request, job_name, build_number):

    jenkins_job = get_object_or_404(JenkinsJob, name=job_name)
    jenkins_build = jenkins_job.builds.filter(number=build_number).prefetch_related("testruns")
    jenkins_umbrella_build = jenkins_build.filter(is_umbrella=True)

    if jenkins_umbrella_build.all():
        jenkins_build = jenkins_umbrella_build

    template = loader.get_template('testrunner/jenkins_build_view.html')

    context = RequestContext(request, {
        'jenkins_build': jenkins_build,
        'lava_url': settings.LAVA_JOB_ID_REGEXP.rsplit("/", 1)[0],
        'statuses': TestStatus.objects.all()
    })
    return HttpResponse(template.render(context))


@login_required
def lava_job_view(request, job_name, build_number, lava_job_number):
    lava_job = get_object_or_404(LavaJob, number=lava_job_number)
    template = loader.get_template('testrunner/lava_job_view.html')
    context = RequestContext(request, {
        'lava_job': lava_job,
        'lava_url': settings.LAVA_JOB_ID_REGEXP.rsplit("/", 1)[0],
    })
    return HttpResponse(template.render(context))


@login_required
def compare_results(request):
    if request.method == "GET":
        form = ResultComparisonForm(request.GET)
        if form.is_valid():
            testsets = form.cleaned_data['testresults']
            testcase_names = LavaJobTestResult.objects.filter(
                lava_job_result__in=testsets).order_by("test_case_id").values("test_case_id").distinct("test_case_id")
            testcase_list = []
            for testcase in testcase_names:
                tc_id = testcase['test_case_id']
                testcase_list.append({'name': tc_id, 'results': [], 'is_different': False})
                for testset in testsets:
                    result = testset.lavajobtestresult_set.filter(test_case_id=tc_id)
                    if result:
                        testcase_list[-1]['results'].append(result[0].status.name) # there should be only one?
                    else:
                        testcase_list[-1]['results'].append("-")
                if len(set(testcase_list[-1]['results'])) > 1:
                    testcase_list[-1]['is_different'] = True

            template = loader.get_template('testrunner/compare_results.html')
            context = RequestContext(request, {
                'testsets': testsets,
                'testcases': testcase_list,
            })
            return HttpResponse(template.render(context))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response


class TagSerializer(serializers.ModelSerializer):
    builds = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag


class BugSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_data')

    class Meta:
        model = Bug

    def get_data(self, obj):
        return obj.get_bug()


class LavaJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = LavaJob


class Tag_ListCreate_View(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    model = Tag


class Tag_Details_View(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    model = Tag


class JenkinsBuild_ListCreate_View(generics.ListCreateAPIView):
    model = JenkinsBuild


class JenkinsBuild_Details_View(generics.RetrieveUpdateDestroyAPIView):
    model = JenkinsBuild


class Trackers_Types_View(APIView):
    def get(self, request, format=None):
        return Response([
            {"name": a, "type": b["type"]} for a,b in settings.TRACKERS.items()
        ])
