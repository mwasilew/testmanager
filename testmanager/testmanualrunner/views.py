from __future__ import unicode_literals
from django.views.generic import TemplateView

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response


from testmanager.testmanualrunner import models
from testmanager.testrunner import models as testrunner_models
from testmanager.testrunner import views as testrunner_views

from testmanager.views import LoginRequiredMixin


class TestRunResultSerializer(serializers.ModelSerializer):
    bugs = testrunner_views.BugSerializer(many=True, read_only=True)
    class Meta:
        model = models.TestRunResult


class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestRun


class JenkinsBuild(serializers.ModelSerializer):
    class Meta:
        model = testrunner_models.JenkinsBuild


class TestStatus(serializers.ModelSerializer):
    class Meta:
        model = models.TestStatus


#### views ####


class Base(LoginRequiredMixin, TemplateView):
    template_name='testmanualrunner.html'


class TestRun_ListCreate_View(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = TestRunSerializer
    model = models.TestRun


class TestRun_Details_View(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestRunSerializer
    model = models.TestRun


class Build_List_View(LoginRequiredMixin, generics.ListAPIView):
    queryset = testrunner_models.JenkinsBuild.objects.all()
    serializer_class = JenkinsBuild


class Build_Details_View(LoginRequiredMixin, generics.RetrieveAPIView):
    queryset = testrunner_models.JenkinsBuild.objects.all()
    serializer_class = JenkinsBuild


class TestStatus_List_View(LoginRequiredMixin, generics.ListAPIView):
    queryset = models.TestStatus.objects.all()
    serializer_class = TestStatus


class TestStatus_Details_View(LoginRequiredMixin, generics.RetrieveAPIView):
    queryset = models.TestStatus.objects.all()
    serializer_class = TestStatus


class TestRunResult_Details_View(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestRunResult.objects.all()
    serializer_class = TestRunResultSerializer


class TestRunResult_ListCreate_View(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = models.TestRunResult.objects.all()
    serializer_class = TestRunResultSerializer
    filter_fields = ('test_run',)


class TestRunResultBug(LoginRequiredMixin, APIView):

    def post(self, request, pk, format=None):
        action = request.DATA.pop('action')
        test_run_result = models.TestRunResult.objects.get(pk=pk)
        bug, _ = testrunner_models.Bug.objects.get_or_create(**request.DATA)
        data = testrunner_views.BugSerializer(bug).data

        if action == "add":
            test_run_result.bugs.add(bug)
            return Response(data)
        else:
            test_run_result.bugs.remove(bug)
            return Response(data)
