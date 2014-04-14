import logging

from django.conf import settings
from django.core.management.base import (
    BaseCommand, 
    CommandError
)
from testrunner.models import LavaJob
from helpers.jenkins_lava import get_lava_job_details

log = logging.getLogger("testrunner")

class Command(BaseCommand):
    def handle(self, *args, **options):
        log.setLevel(logging.DEBUG)
        for job in LavaJob.objects.filter(status__name__in=settings.LAVA_JOB_RUNNING_STATUSES):
            log.debug("checking LAVA job {0}".format(job.number))
            get_lava_job_details(job.number, job.jenkins_build)


