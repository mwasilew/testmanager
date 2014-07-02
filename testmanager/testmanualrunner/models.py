from django.db import models


class TestRun(models.Model):
    test_plan = models.ForeignKey('testplanner.TestPlan')
    created_at = models.DateField(auto_now_add=True)


class TestRunResult(models.Model):
    test_run = models.ForeignKey('TestRun')
    test_definition = models.ForeignKey('testplanner.TestDefinition')
    created_at = models.DateField(auto_now_add=True)

