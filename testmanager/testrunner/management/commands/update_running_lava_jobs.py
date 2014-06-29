# Copyright (C) 2014 Linaro Limited
#
# Author: Milosz Wasilewski <milosz.wasilewski@linaro.org>
#
# This file is part of Testmanager.
#
# Testmanager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation
#
# Testmanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Testmanager.  If not, see <http://www.gnu.org/licenses/>.

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from testmanager.testrunner.models import LavaJob
from helpers.jenkins_lava import get_lava_job_details


log = logging.getLogger("testrunner")


class Command(BaseCommand):
    def handle(self, *args, **options):
        log.setLevel(logging.DEBUG)
        for job in LavaJob.objects.filter(status__name__in=settings.LAVA_JOB_RUNNING_STATUSES):
            log.debug("checking LAVA job {0}".format(job.number))
            get_lava_job_details(job.number, job.jenkins_build)


