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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader

from testplanner.models import *
from testrunner.models import (
    JenkinsJob
)


@login_required
def default(request):
    jenkins_jobs = JenkinsJob.objects.all().order_by("name")
    context = RequestContext(request, {
        'jenkins_jobs': jenkins_jobs,
    })
    template = loader.get_template('testdashboard/index.html') 
    return HttpResponse(template.render(context))

