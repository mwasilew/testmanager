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

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from django_dynamic_fixture import G

from testmanager.testplanner import models


class TestTestPlan(APITestCase):

    def test_create_test_plan(self):
        self.client.force_authenticate(user=G(User))

        device = G(models.Device)

        data = {
            "name": "test",
            "description": "test",
            "device": device.id,
            "tests_definitions": [
                G(models.TestDefinition).id for _ in range(10)
            ]
        }

        response = self.client.post("/planner/view/plan/", data)

        test_plan = models.TestPlan.objects.get(name=data['name'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.TestPlan.objects.count(), 1)
        self.assertEqual(test_plan.testplantestdefinition_set.count(), 10)

    def test_get_test_plan(self):
        self.client.force_authenticate(user=G(User))

        test_plan = G(models.TestPlan)

        for i in range(10):
            G(models.TestPlanTestDefinition, test_plan=test_plan)

        response = self.client.get("/planner/view/plan/%s/" % test_plan.id)

        self.assertEqual(len(response.data['tests_definitions']), 10)

    def test_update_test_plan(self):
        self.client.force_authenticate(user=G(User))

        test_plan = G(models.TestPlan)

        for i in range(10):
            G(models.TestPlanTestDefinition, test_plan=test_plan)

        self.assertEqual(test_plan.testplantestdefinition_set.count(), 10)

        data = {
            "name": test_plan.name,
            "device": test_plan.device.id,
            "description": test_plan.description,
            "tests_definitions": [
                G(models.TestDefinition).id for _ in range(2)
            ]
        }

        self.client.put("/planner/view/plan/%s/" % test_plan.id, data)

        self.assertEqual(models.TestPlan.objects.count(), 1)
        self.assertEqual(test_plan.testplantestdefinition_set.count(), 2)
