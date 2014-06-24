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

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testplanner.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'testdashboard.views.default'),
    (r'^testrunner/',
        include('testrunner.urls', app_name="testrunner")),
    (r'^testplanner/',
        include('testplanner.urls', app_name="testplanner")),

    url(r'^admin/', include(admin.site.urls)),

    # Login
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
     {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/'}),

)
