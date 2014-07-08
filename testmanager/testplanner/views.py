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
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status

from testmanager.testplanner import models


class Base(TemplateView):
    template_name='testplanner.html'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device


class TestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestPlan

    owner = serializers.RelatedField()
    tests_definitions = serializers.SerializerMethodField('get_tests_definitions')

    def __init__(self, instance=None, data=None, *args, **kwargs):
        if data:
            self.tests_definitions = data.pop('tests_definitions', [])
        else:
            self.tests_definitions = []

        super(TestPlanSerializer, self).__init__(instance, data, *args, **kwargs)

    def save_object(self, obj, **kwargs):
        obj.save(**kwargs)
        obj.testplantestdefinition_set.all().delete()
        for test_definition_id in self.tests_definitions:
            models.TestPlanTestDefinition.objects.create(
                test_plan=obj,
                test_definition_id=test_definition_id
            )

    def get_tests_definitions(self, obj):
        query = models.TestDefinition.objects.filter(
            testplantestdefinition__test_plan=obj
        )
        serialize = TestDefinitionSerializer(query)
        return serialize.data


class TestDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestDefinition
        fields = ('id', 'name', 'test_id', 'test_file_name')


class DefinitionView(APIView):
    serializer_class = TestDefinitionSerializer

    def get(self, request, device_id, format=None):
        query = models.TestDefinition.objects.filter(device__id=device_id)
        serializer = self.serializer_class(query)
        return Response(serializer.data)


class TestPlanView(generics.ListCreateAPIView):
    queryset = models.TestPlan.objects.all()
    serializer_class = TestPlanSerializer

    def post(self, request, format=None):
        serializer = TestPlanSerializer(data=request.DATA)

        if serializer.is_valid():
            serializer.object.owner = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestPlanDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestPlan.objects.all()
    serializer_class = TestPlanSerializer


class DeviceView(generics.ListCreateAPIView):
    serializer_class = DeviceSerializer
    queryset = models.Device.objects.all()


class DeviceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer
    queryset = models.Device.objects.all()


