from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status

from testmanager.testmanualrunner import models


class Base(TemplateView):
    template_name='testmanualrunner/base.html'


class TestRun(serializers.ModelSerializer):
    class Meta:
        model = models.TestRun


class TestRunResult(serializers.ModelSerializer):
    class Meta:
        model = models.TestRunResult


class TestRun_ListCreate_View(generics.ListCreateAPIView):
    queryset = models.TestRun.objects.all()
    serializer_class = TestRun


class TestRun_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestRun.objects.all()
    serializer_class = TestRun



