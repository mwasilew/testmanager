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
import yaml
from os import path
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from testmanager.views import LoginRequiredMixin
from testmanager.testplanner import models
from testmanager.testplanner import serializers


class Base(LoginRequiredMixin, TemplateView):
    template_name='testplanner.html'


class DefinitionView(LoginRequiredMixin, APIView):
    serializer_class = serializers.TestDefinitionSerializer

    def get(self, request, device_id, format=None):
        query = models.TestDefinition.objects.filter(device__id=device_id, is_automated=False)
        serializer = self.serializer_class(query)
        return Response(serializer.data)


class Definition_Yaml_View(LoginRequiredMixin, APIView):

    def get(self, request, pk, format=None):
        obj = models.TestDefinition.objects.get(pk=pk)
        location = path.join(obj.repository.local_dir, obj.test_file_name)
        yaml_file = open(location,'r').read()
        yaml_content = yaml.load(yaml_file)
        return Response({
            "yaml": {'description': yaml_content['metadata'].get('description', ''),
                     'steps': [x.replace("\n", "<br/>") for x in yaml_content['run'].get('steps', '')],
                     'expected': [x.replace("\n", "<br/>") for x in yaml_content['run'].get('expected', '')],
                     'metadata': yaml_content['metadata'],
                    }
        })


class TestPlanView(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = models.TestPlan.objects.all()
    serializer_class = serializers.TestPlanSerializer

    def post(self, request, format=None):
        serializer = serializers.TestPlanSerializer(data=request.DATA)

        if serializer.is_valid():
            serializer.object.owner = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestPlanDetails(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestPlan.objects.all()
    serializer_class = serializers.TestPlanSerializer

    def post_save(self, obj, created):
        for testrun in obj.testrun_set.all():
            testrun.save()


class DeviceView(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = serializers.DeviceSerializer
    model = models.Device


class DeviceDetailsView(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.DeviceSerializer
    queryset = models.Device.objects.all()

