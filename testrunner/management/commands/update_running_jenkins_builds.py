import logging
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.requester import Requester
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
            # dirty hack to overcome SSL issues with Linaro Jenkins
            requester = Requester(baseurl=build.job.service.url, ssl_verify=False)
            jenkins = Jenkins(build.job.service.url, requester=requester)
            #jenkins = Jenkins(build.job.service.url)
            jenkins_job = jenkins[build.job.name]
            #log.debug("checking Jenkins build {0}".format(build.name.decode('ascii', 'ignore')))
            log.debug("checking Jenkins build {0}".format(''.join([x for x in build.name if ord(x) < 128])))
            fetch_jenkins_builds(build.job, jenkins_job, build.number)
