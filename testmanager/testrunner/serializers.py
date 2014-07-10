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
from testmanager.testrunner import models


class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JenkinsBuild


class TagSerializer(serializers.ModelSerializer):
    builds = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Tag


class LavaJobResultSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='test_definition.name')
    results = serializers.Field(source='get_resultset_count_by_status')

    class Meta:
        model = models.LavaJobResult


class LavaJobSerializer(serializers.ModelSerializer):
    results = LavaJobResultSerializer(source="lavajobresult_set", many=True)

    class Meta:
        model = models.LavaJob


class BugSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_data')

    class Meta:
        model = models.Bug

    def get_data(self, obj):
        return obj.get_bug()
