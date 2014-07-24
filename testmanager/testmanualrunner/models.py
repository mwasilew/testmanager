from django.db import models
from testmanager.testrunner.models import Bug


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
                self.results.filter(status__name=status).count()
            ))

        return ret

    def get_run_results(self):
        return self.results.all()

    def get_bug_count(self):
        b = Bug.objects.filter(testrunresult__in=list(self.results.all()))
        return b.distinct().count()

    def update_results(self):
        test_definition_restuls_ids = self.results\
                                          .values_list('test_definition', flat=True)
        # execute this code only on initial object creation
        if not test_definition_restuls_ids:
            test_definition_ids = self.test_plan.testplantestdefinition_set\
                                                .values_list('test_definition_id', flat=True)


            for test_definition_id in set(test_definition_ids) - set(test_definition_restuls_ids):
                TestRunResult.objects.create(
                    test_run=self,
                    test_definition_id=test_definition_id
                )

            for test_definition_id in set(test_definition_restuls_ids) - set(test_definition_ids):
                TestRunResult.objects.get(
                    test_run=self,
                    test_definition_id=test_definition_id
                ).delete()

    def save(self, *args, **kwargs):
        super(TestRun, self).save(*args, **kwargs)
        self.update_results()


class TestRunResult(models.Model):
    class Meta:
        unique_together = ("test_run", "test_definition")

    test_run = models.ForeignKey('TestRun', related_name='results')
    test_definition = models.ForeignKey('testplanner.TestDefinition')
    # add revision field so the proper data is taken into use
    #test_definition_revision = models.ForeignKey('testplanner.TestDefinitionRevision')

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
