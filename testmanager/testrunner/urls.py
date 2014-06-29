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

from django.conf.urls import patterns, url, include
from testmanager.testrunner import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index),

    url(r'^jenkins_job/(?P<job_name>[0-9a-zA-Z_\-]+)$',
        views.jenkins_job_view, name='jenkins_job_view'),

    # url(r'^jenkins_job/build/(?P<build_name>[a-zA-Z_\-]+)',
    #     jenkins_build_list, name='jenkins_build_list'),

    url(r'^jenkins_job/(?P<job_name>[0-9a-zA-Z_\-]+)/build/(?P<build_number>\d+)$',
        views.jenkins_build_view, name='jenkins_build_view'),

    url(r'^jenkins_job/(?P<job_name>[0-9a-zA-Z_\-]+)/build/(?P<build_number>\d+)/(?P<lava_job_number>\d+)$',
        views.lava_job_view, name='lava_job_view'),

    # compare test results
    url(r'^compare_results/$', views.compare_results, name='compare_results'),
)
