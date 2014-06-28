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


from testrunner.models import JenkinsJob
from django.views.generic import TemplateView


class Main(TemplateView):
    template_name='testdashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context['jenkins_jobs'] = JenkinsJob.objects.order_by("name")
        return context
