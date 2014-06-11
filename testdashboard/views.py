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

