from django.db import models


class TestRun(models.Model):
    test_plan = models.ForeignKey('testplanner.TestPlan')
    build = models.ForeignKey('testrunner.JenkinsBuild', related_name="testruns")

    closed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_results(self):
        statuses = TestStatus.objects.all().values_list("name", flat=True)
        ret = []
        for status in statuses:
            ret.append((
                status,
                self.tests_definitions_results.filter(status__name=status).count()
            ))

        return ret


    def save(self, *args, **kwargs):
        created = self.id
        super(TestRun, self).save(*args, **kwargs)

        if not created:
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
    bugs = models.ManyToManyField('testrunner.Bug', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestStatus(models.Model):
    name = models.CharField(max_length=36)
    color = models.CharField(max_length=36)
    icon = models.CharField(blank=True, max_length=36)

    def __unicode__(self):
        return self.name
