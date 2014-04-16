import logging

from django.conf import settings
from django.core.management.base import (
    BaseCommand, 
    CommandError
)
from testrunner.models import JenkinsJob
from jenkinsapi.jenkins import Jenkins
from helpers.jenkins_lava import (
    fetch_jenkins_builds
)

#log = logging.getLogger('testrunner.fetch_matrix_builds')
log = logging.getLogger('testrunner')


class Command(BaseCommand):
    def handle(self, *args, **options):
        log.setLevel(logging.DEBUG)
        for job in JenkinsJob.objects.all():
            log.debug("processing {0}".format(job.name))
            jenkins = Jenkins(job.service.url)
            jenkins_job = jenkins[job.name]
            last_db_build = job.builds.filter(is_umbrella=True).order_by('-number')
            if not last_db_build:
                # make sure there are not builds if this is not a matrix type job
                # if there are no builds at all, the result is the same
                last_db_build = job.builds.filter(is_umbrella=False).order_by('-number')
            last_jenkins_build = jenkins_job.get_last_buildnumber()
            if last_db_build: 
                if last_db_build[0].number < last_jenkins_build:
                    for jenkins_build in range(last_db_build[0].number + 1, last_jenkins_build + 1):
                        log.debug("jenkins_build to fetch: {0}".format(jenkins_build))
                        fetch_jenkins_builds(job, jenkins_job, jenkins_build)

            else: # no builds in db ?
                for jenkins_build in range(jenkins_job.get_first_buildnumber(), last_jenkins_build + 1):
                    fetch_jenkins_builds(job, jenkins_job, jenkins_build)
