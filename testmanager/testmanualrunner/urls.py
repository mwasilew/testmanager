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
from testmanager.testmanualrunner import views


urlpatterns = [
    url(r'view/testrun/$', views.TestRun_ListCreate_View.as_view()),
    url(r'view/testrun/(?P<pk>[0-9]+)/$', views.TestRun_Details_View.as_view()),

    url(r'view/build/$', views.Build_List_View.as_view()),
    url(r'view/build/(?P<pk>[0-9]+)/$', views.Build_Details_View.as_view()),

    url(r'view/status/$', views.TestStatus_List_View.as_view()),
    url(r'view/status/(?P<pk>[0-9]+)/$', views.TestStatus_Details_View.as_view()),

    url(r'view/testrunresult/(?P<pk>[0-9]+)/$', views.TestRunResult_Details_View.as_view()),
    url(r'view/testrunresult/$', views.TestRunResult_ListCreate_View.as_view()),

    url(r'view/testrunresult/(?P<pk>[0-9]+)/bug/$', views.TestRunResultBug.as_view()),

    url(r'$', views.Base.as_view()),
]
