from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from testrunner.models import (
    JenkinsJob,
    JenkinsBuild,
    LavaJob,
)


@login_required
def index(request):
    jenkins_jobs = JenkinsJob.objects.all()
    template = loader.get_template('testrunner/index.html')
    context = RequestContext(request, {
        'jenkins_jobs': jenkins_jobs,
    })
    return HttpResponse(template.render(context))

@login_required
def jenkins_job_view(request, job_name):
    jenkins_job = get_object_or_404(JenkinsJob, name=job_name)
    jenkins_builds = jenkins_job.builds.filter(is_umbrella=False).order_by("-pk")[:30]
    template = loader.get_template('testrunner/jenkins_job_view.html')
    context = RequestContext(request, {
        'jenkins_job': jenkins_job,
        'jenkins_builds': jenkins_builds 
    })
    return HttpResponse(template.render(context))   

@login_required
def jenkins_build_view(request, job_name, build_number):
    jenkins_job = get_object_or_404(JenkinsJob, name=job_name)
    jenkins_build = jenkins_job.builds.filter(number = build_number)
    jenkins_umbrella_build = jenkins_build.filter(is_umbrella = True)
    if jenkins_umbrella_build.all():
        jenkins_build = jenkins_umbrella_build
    template = loader.get_template('testrunner/jenkins_build_view.html')
    context = RequestContext(request, {
        'jenkins_build': jenkins_build,
        'lava_url': settings.LAVA_JOB_ID_REGEXP.rsplit("/", 1)[0],
    })
    return HttpResponse(template.render(context))

@login_required
def lava_job_view(request, job_name, build_number, lava_job_number):
    lava_job = get_object_or_404(LavaJob, number=lava_job_number)
    template = loader.get_template('testrunner/lava_job_view.html')
    context = RequestContext(request, {
        'lava_job': lava_job,
        'lava_url': settings.LAVA_JOB_ID_REGEXP.rsplit("/", 1)[0],
    })
    return HttpResponse(template.render(context))   
