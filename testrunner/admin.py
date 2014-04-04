from django.contrib import admin
from testrunner.models import (
    JenkinsService,
    JenkinsJob,
    JenkinsBuildStatus,
    JenkinsBuild,
    LavaJobStatus,
    LavaJob,
    LavaJobResultStatus,
    LavaJobResult,
    LavaJobTestResultUnit,
    LavaJobTestResult
)

admin.site.register(JenkinsService)
admin.site.register(JenkinsJob)
admin.site.register(JenkinsBuildStatus)
admin.site.register(JenkinsBuild)
admin.site.register(LavaJobStatus)
admin.site.register(LavaJob)
admin.site.register(LavaJobResultStatus)
admin.site.register(LavaJobResult)
admin.site.register(LavaJobTestResultUnit)
admin.site.register(LavaJobTestResult)
