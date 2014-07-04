from django.test import TestCase
from django_dynamic_fixture import G

from testmanager.testmanualrunner.models import TestRun, TestRunResult
from testmanager.testplanner.models import TestPlan, TestPlanTestDefinition
from testmanager.testrunner.models import JenkinsBuild
# Create your tests here.

class TestTestRun(TestCase):

    def test_testrun_create(self):
        test_plan = G(TestPlan)
        build = G(JenkinsBuild)

        for i in range(10):
            G(TestPlanTestDefinition, test_plan=test_plan)

        test_run = TestRun.objects.create(
            test_plan=test_plan,
            build=build
        )

        self.assertEqual(TestRunResult.objects.filter(test_run=test_run).count(), 10)
