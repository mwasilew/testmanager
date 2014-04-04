from django.contrib import admin
from testplanner.models import (
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
