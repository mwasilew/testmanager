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
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.requester import Requester
from django.conf import settings
from django.core.management.base import BaseCommand
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
