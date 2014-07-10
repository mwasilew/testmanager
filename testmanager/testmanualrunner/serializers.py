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

from rest_framework import serializers
from testmanager.testmanualrunner import models
from testmanager.testrunner.serializers import BugSerializer
from testmanager.testplanner.serializers import TestPlanSerializer


class TestRunSerializer(serializers.ModelSerializer):
    result = serializers.Field(source='get_results')
    test_plan = TestPlanSerializer()

    class Meta:
        model = models.TestRun


class TestRunResultSerializer(serializers.ModelSerializer):
    bugs = BugSerializer(many=True, read_only=True)
    class Meta:
        model = models.TestRunResult


class TestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestStatus

