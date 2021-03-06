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
from testmanager.testplanner.models import (
    TestRepository,
    Maintainer,
    OS,
    Scope,
    Device,
    TestPlan,
    TestDefinition,
    TestDefinitionRevision,
    TestPlanTestDefinition
)

admin.site.register(TestRepository)
admin.site.register(Maintainer)
admin.site.register(OS)
admin.site.register(Scope)
admin.site.register(Device)
admin.site.register(TestPlan)
admin.site.register(TestDefinition)
admin.site.register(TestDefinitionRevision)
admin.site.register(TestPlanTestDefinition)
