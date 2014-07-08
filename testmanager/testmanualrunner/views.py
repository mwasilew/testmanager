from __future__ import unicode_literals
from django.views.generic import TemplateView

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView

from testmanager.testmanualrunner import models
from testmanager.testrunner import models as testrunner_models


class Base(TemplateView):
    template_name='testmanualrunner.html'


class TestRunResult(serializers.ModelSerializer):
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


class TestRun_ListCreate_View(generics.ListCreateAPIView):
    serializer_class = TestRunSerializer
    model = models.TestRun


class TestRun_Details_View(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestRunSerializer
    model = models.TestRun


class Build_List_View(generics.ListAPIView):
    queryset = testrunner_models.JenkinsBuild.objects.all()
    serializer_class = JenkinsBuild


class Build_Details_View(generics.RetrieveAPIView):
    queryset = testrunner_models.JenkinsBuild.objects.all()
    serializer_class = JenkinsBuild


class TestStatus_List_View(generics.ListAPIView):
    queryset = models.TestStatus.objects.all()
    serializer_class = TestStatus


class TestStatus_Details_View(generics.RetrieveAPIView):
    queryset = models.TestStatus.objects.all()
    serializer_class = TestStatus


class TestRunResult_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestRunResult.objects.all()
    serializer_class = TestRunResult


class TestRunResult_ListCreate_View(generics.ListCreateAPIView):
    queryset = models.TestRunResult.objects.all()
    serializer_class = TestRunResult
    filter_fields = ('test_run',)


class Bug(APIView):

    def post(self, request, testrunresult_pk, format=None):
        import pdb; pdb.set_trace()

    def delete(self, request, testrunresult_pk, format=None):
        import pdb; pdb.set_trace()
