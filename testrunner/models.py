import re
from django.db import models
from django.core.urlresolvers import reverse

class JenkinsService(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.url)


class JenkinsJob(models.Model):
    name = models.CharField(max_length=128)
    service = models.ForeignKey(JenkinsService)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jenkins_job_view', args=[str(self.name)])


class JenkinsBuildStatus(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


class JenkinsBuild(models.Model):
    name = models.CharField(max_length=1024)
    job = models.ForeignKey(JenkinsJob, related_name="builds")
    umbrella_build = models.ForeignKey("self", blank=True, null=True)
    number = models.IntegerField()
    status = models.ForeignKey(JenkinsBuildStatus)
    is_umbrella = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jenkins_build_view', args=[str(self.job.name), str(self.number)])

    def get_hwpack_name(self):
        if self.is_umbrella:
            return None
        device_regexp = re.compile(ur'%s\s\xbb\s(?P<device_name>\w+)' % (self.job.name), re.UNICODE)
        hwpack_name_search = device_regexp.search(self.name)
        if hwpack_name_search:
            return hwpack_name_search.group('device_name')
        return None


class LavaJobStatus(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


class LavaJob(models.Model):
    jenkins_build = models.ForeignKey(JenkinsBuild)
    number = models.IntegerField()
    status = models.ForeignKey(LavaJobStatus)
    test_definitions = models.ManyToManyField('testplanner.TestDefinition')
    device_type = models.ForeignKey('testplanner.Device')
    submit_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s - LAVA %s" % (self.jenkins_build.job.name, self.number)

    def get_definitions_results(self):
        result_list = []
        for testdef in self.test_definitions.all():
            resultset = LavaJobResult.objects.filter(lava_job = self, test_definition = testdef)
            if resultset:
                result_list.append((testdef, resultset[0]))
            else:
                result_list.append((testdef, None))
        return result_list

    # TODO: move to helpers to be defined during import time, include field for failed tests
    def has_results_missing(self):
        for testdef in self.test_definitions.all():
            resultset = LavaJobResult.objects.filter(lava_job = self, test_definition = testdef)
            if not resultset:
                return True
        return False

    def get_absolute_url(self):
        return reverse('lava_job_view', args=[str(self.jenkins_build.job.name), str(self.jenkins_build.number), str(self.number)])


class LavaJobResultStatus(models.Model):
    name = models.CharField(max_length=8)

    def __unicode__(self):
        return self.name


class LavaJobResult(models.Model):
    lava_job = models.ForeignKey(LavaJob)
    test_definition = models.ForeignKey('testplanner.TestDefinition')
    test_revision = models.ForeignKey('testplanner.TestDefinitionRevision', blank=True, null=True)

    def __unicode__(self):
        return "%s result for %s" % (self.lava_job.__unicode__(), self.test_definition.__unicode__())

    def get_resultset_total(self):
        return self.lavajobtestresult_set.count()
    
    def get_resultset_count_by_status(self):
        status_count = {}
        # TODO: fix this, use aggregate to collect the numbers
        for testresult in self.lavajobtestresult_set.all():
            if testresult.status.name in status_count:
                status_count[testresult.status.name] += 1
            else:
                status_count[testresult.status.name] = 1
        print status_count
        return status_count
                

class LavaJobTestResultUnit(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class LavaJobTestResult(models.Model):
    test_case_id = models.CharField(max_length=1024)
    lava_job_result = models.ForeignKey(LavaJobResult)
    status = models.ForeignKey(LavaJobResultStatus, blank=True, null=True) # there should be default of 'unknown'
    is_measurement = models.BooleanField(default=False)
    unit = models.ForeignKey(LavaJobTestResultUnit, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.test_case_id

class LavaJobTestResultUnit(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class LavaJobTestResult(models.Model):
    test_case_id = models.CharField(max_length=1024)
    lava_job_result = models.ForeignKey(LavaJobResult)
    status = models.ForeignKey(LavaJobResultStatus, blank=True, null=True) # there should be default of 'unknown'
    is_measurement = models.BooleanField(default=False)
    unit = models.ForeignKey(LavaJobTestResultUnit, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.test_case_id
