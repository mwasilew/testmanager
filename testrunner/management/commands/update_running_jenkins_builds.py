import logging
from jenkinsapi.jenkins import Jenkins
from django.conf import settings
from django.core.management.base import (
    BaseCommand, 
    CommandError
)
from helpers.jenkins_lava import fetch_jenkins_builds
from testrunner.models import JenkinsBuild 

log = logging.getLogger('testrunner')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for build in JenkinsBuild.objects.filter(status__name__in=settings.JENKINS_BUILD_RUNNING_STATUSES):
            jenkins = Jenkins(build.job.service.url)
            jenkins_job = jenkins[build.job.name]
            log.debug("checking Jenkins build {0}".format(build.name))
            fetch_jenkins_builds(build.job, jenkins_job, build.number)
