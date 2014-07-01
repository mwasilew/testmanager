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


from django.utils.text import slugify
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

    class Meta:
        model = models.TestPlan


class TestPlanView(APIView):

    def get(self, request, format=None):
        serializer = TestPlanSerializer(models.TestPlan.objects.all())
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.DATA
        data['slug'] = slugify(request.DATA['name'])
        data['owner'] = request.user.pk

        serializer = TestPlanSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceView(generics.ListCreateAPIView):
    serializer_class = DeviceSerializer
    queryset = models.Device.objects.all()


