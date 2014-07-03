from django.db import models


class TestRun(models.Model):
    test_plan = models.ForeignKey('testplanner.TestPlan')
    build = models.ForeignKey('testrunner.JenkinsBuild')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestRunResult(models.Model):
    test_run = models.ForeignKey('TestRun')
    test_definition = models.ForeignKey('testplanner.TestDefinition')

    status = models.ForeignKey('TestStatus')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestStatus(models.Model):
    name = models.CharField(max_length=36)
    color = models.CharField(max_length=36)
