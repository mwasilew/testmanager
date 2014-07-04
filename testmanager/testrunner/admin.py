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
from testmanager.testrunner import models

admin.site.register(models.JenkinsService)
admin.site.register(models.JenkinsJob)
admin.site.register(models.JenkinsBuildStatus)
admin.site.register(models.JenkinsBuild)
admin.site.register(models.LavaJobStatus)
admin.site.register(models.LavaJob)
admin.site.register(models.LavaJobResultStatus)
admin.site.register(models.LavaJobResult)
admin.site.register(models.LavaJobTestResultUnit)
admin.site.register(models.LavaJobTestResult)
admin.site.register(models.Bug)
