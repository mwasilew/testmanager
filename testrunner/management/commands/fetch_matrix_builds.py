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
            log.debug(last_db_build)
            last_jenkins_build = jenkins_job.get_last_buildnumber()
            build_ids = []
            for build_id in jenkins_job.get_build_ids():
                if last_db_build:
                    if build_id > last_db_build[0].number:
                        build_ids.insert(0, build_id)
                else:
                    build_ids.insert(0, build_id)
            log.debug("build IDs")
            log.debug(build_ids)
            for jenkins_build in build_ids:
                log.debug("jenkins_build to fetch: {0}".format(jenkins_build))
                fetch_jenkins_builds(job, jenkins_job, jenkins_build)
