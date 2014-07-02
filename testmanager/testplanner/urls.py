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
from testmanager.testplanner import views


urlpatterns = [
    url(r'view/plan/$', views.TestPlanView.as_view()),
    url(r'view/plan/(?P<pk>[0-9]+)/$', views.TestPlanDetails.as_view()),

    url(r'view/device/', views.DeviceView.as_view()),
    url(r'view/definitions/(?P<device_name>.+)/', views.DefinitionView.as_view()),

    url(r'^$', views.Base.as_view()),
]
