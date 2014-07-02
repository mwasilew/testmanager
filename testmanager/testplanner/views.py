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
    template_name='testplanner/base.html'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device


class TestPlanSerializer(serializers.ModelSerializer):
    owner = serializers.RelatedField()
    device = DeviceSerializer()
    test_definitions = serializers.SerializerMethodField('get_test_definitions')

    class Meta:
        model = models.TestPlan

    def get_test_definitions(self, obj):
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

    def get(self, request, device_name, format=None):
        query = models.TestDefinition.objects.filter(device__name=device_name)
        serializer = self.serializer_class(query)
        return Response(serializer.data)


class TestPlanView(generics.ListCreateAPIView):
    queryset = models.TestPlan.objects.all()
    serializer_class = TestPlanSerializer

    def post(self, request, format=None):
        serializer = TestPlanSerializer(data=request.DATA)
        definitions = request.DATA.pop('definitions', [])

        if serializer.is_valid():
            serializer.object.owner = request.user
            serializer.save()

            for test_definition_id in definitions:
                models.TestPlanTestDefinition.objects.create(
                    test_plan=serializer.object,
                    test_definition_id=test_definition_id
                )

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


