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

from __future__ import unicode_literals
from django.views.generic import TemplateView

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from testmanager.views import LoginRequiredMixin
from testmanager.testmanualrunner import models
from testmanager.testrunner import models as testrunner_models

from testmanager.testmanualrunner.serializers import (
    TestStatusSerializer, TestRunSerializer, TestRunResultSerializer
)
from testmanager.testrunner.serializers import BugSerializer


class Base(LoginRequiredMixin, TemplateView):
    template_name='testmanualrunner.html'


class TestRun_ListCreate_View(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = TestRunSerializer
    model = models.TestRun


class TestRun_Details_View(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestRunSerializer
    model = models.TestRun


class TestStatus_List_View(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = TestStatusSerializer
    model = models.TestStatus


class TestStatus_Details_View(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = TestStatusSerializer
    model = models.TestStatus


class TestRunResult_Details_View(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestRunResultSerializer
    model = models.TestRunResult


class TestRunResult_ListCreate_View(LoginRequiredMixin, generics.ListCreateAPIView):
    model = models.TestRunResult
    serializer_class = TestRunResultSerializer
    filter_fields = ('test_run',)


class TestRunResultBug(LoginRequiredMixin, APIView):

    def post(self, request, pk, format=None):
        action = request.DATA.pop('action')
        test_run_result = models.TestRunResult.objects.get(pk=pk)
        bug, _ = testrunner_models.Bug.objects.get_or_create(**request.DATA)
        data = BugSerializer(bug).data

        if action == "add":
            test_run_result.bugs.add(bug)
            return Response(data)
        else:
            test_run_result.bugs.remove(bug)
            return Response(data)

