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

from testmanager.views import LoginRequiredMixin
from testmanager.testrunner.models import LavaJob, Tag
from testmanager.testrunner.serializers import BuildSerializer, TagSerializer, LavaJobSerializer


class Base(LoginRequiredMixin, TemplateView):
    template_name='testreporter/base.html'


class Report_View(LoginRequiredMixin, APIView):

    def get(self, request, tag_id, format=None):
        tag = Tag.objects.get(id=tag_id).prefetch_related('builds')
        lava_jobs = LavaJob.objects.filter(jenkins_build__in=tag.builds)

        return Response({
            "tag": TagSerializer(tag).data,
            "builds": BuildSerializer(tag.builds).data,
            "lava_jobs": LavaJobSerializer(lava_jobs).data,
        })
