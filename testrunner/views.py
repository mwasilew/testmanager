from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from testrunner.models import (
    JenkinsJob,
    JenkinsBuild,
)


def index(request):
    jenkins_jobs = JenkinsJob.objects.all()
    template = loader.get_template('testrunner/index.html')
    context = RequestContext(request, {
        'jenkins_jobs': jenkins_jobs,
    })
    return HttpResponse(template.render(context))

def jenkins_job_view(request, job_name):
    jenkins_job = get_object_or_404(JenkinsJob, name=job_name)
    template = loader.get_template('testrunner/jenkins_job_view.html')
    context = RequestContext(request, {
        'jenkins_job': jenkins_job,
    })
    return HttpResponse(template.render(context))   

def jenkins_build_view(request, job_name, build_number):
    print job_name, build_number
    jenkins_job = get_object_or_404(JenkinsJob, name=job_name)
    jenkins_build = jenkins_job.builds.filter(is_umbrella = True, number = build_number)
    template = loader.get_template('testrunner/jenkins_build_view.html')
    context = RequestContext(request, {
        'jenkins_build': jenkins_build,
        'lava_url': settings.LAVA_JOB_ID_REGEXP.rsplit("/", 1)[0],
    })
    return HttpResponse(template.render(context))   
