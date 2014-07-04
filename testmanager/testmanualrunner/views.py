from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status

from testmanager.testmanualrunner import models
from testmanager.testrunner import models as testrunner_models


class Base(TemplateView):
    template_name='testmanualrunner/base.html'


#### serializers ####


class TestRun(serializers.ModelSerializer):
    class Meta:
        model = models.TestRun


class JenkinsBuild(serializers.ModelSerializer):
    class Meta:
        model = testrunner_models.JenkinsBuild


class TestRunResult(serializers.ModelSerializer):
    class Meta:
        model = models.TestRunResult


#### views ####


class TestRun_ListCreate_View(generics.ListCreateAPIView):
    queryset = models.TestRun.objects.all()
    serializer_class = TestRun


class TestRun_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestRun.objects.all()
    serializer_class = TestRun


class Build_List_View(generics.ListAPIView):
    queryset = testrunner_models.JenkinsBuild.objects.all()
    serializer_class = JenkinsBuild


class Build_Details_View(generics.RetrieveAPIView):
    queryset = testrunner_models.JenkinsBuild.objects.all()
    serializer_class = JenkinsBuild



