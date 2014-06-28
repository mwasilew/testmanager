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

from django.contrib import admin
from testrunner.models import (
    JenkinsService,
    JenkinsJob,
    JenkinsBuildStatus,
    JenkinsBuild,
    LavaJobStatus,
    LavaJob,
    LavaJobResultStatus,
    LavaJobResult,
    LavaJobTestResultUnit,
    LavaJobTestResult
)

admin.site.register(JenkinsService)
admin.site.register(JenkinsJob)
admin.site.register(JenkinsBuildStatus)
admin.site.register(JenkinsBuild)
admin.site.register(LavaJobStatus)
admin.site.register(LavaJob)
admin.site.register(LavaJobResultStatus)
admin.site.register(LavaJobResult)
admin.site.register(LavaJobTestResultUnit)
admin.site.register(LavaJobTestResult)
