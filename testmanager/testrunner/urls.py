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

from django.conf.urls import url
from testmanager.testrunner import views

urlpatterns = [
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


    url(r'^tag/$', views.Tag_ListCreate_View.as_view()),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.Tag_Details_View.as_view()),

    url(r'^build/(?P<pk>[0-9]+)/$', views.JenkinsBuild_Details_View.as_view()),
    url(r'^build/$', views.JenkinsBuild_ListCreate_View.as_view()),

    url(r'^lavajob/(?P<number>[0-9]+)/$', views.LavaJob_Details_View.as_view()),
    url(r'^lavajob/(?P<number>[0-9]+)/bug/$', views.LavaJobBug.as_view()),

    url(r'^trackers/$', views.Trackers_Types_View.as_view()),
    url(r'^fetch-lavajob/(?P<build_id>[0-9]+)/(?P<lavajob_id>[0-9]+)/$', views.Fetch_LavaJob.as_view()),

]
