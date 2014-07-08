from django.db import models


class TestRun(models.Model):
    test_plan = models.ForeignKey('testplanner.TestPlan')
    build = models.ForeignKey('testrunner.JenkinsBuild')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(TestRun, self).save(*args, **kwargs)

        for testplan_testdefinition in self.test_plan.testplantestdefinition_set.all():
            TestRunResult.objects.create(
                test_run=self,
                test_definition=testplan_testdefinition.test_definition
            )


class TestRunResult(models.Model):
    class Meta:
        unique_together = ("test_run", "test_definition")

    test_run = models.ForeignKey('TestRun', related_name='tests_definitions_results')
    test_definition = models.ForeignKey('testplanner.TestDefinition')

    status = models.ForeignKey('TestStatus', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestStatus(models.Model):
    name = models.CharField(max_length=36)
    color = models.CharField(max_length=36)
    icon = models.CharField(blank=True, max_length=36)

    def __unicode__(self):
        return self.name
