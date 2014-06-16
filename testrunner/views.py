from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseServerError,
    HttpResponseRedirect
)
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from testrunner.models import (
    JenkinsJob,
    JenkinsBuild,
    LavaJob,
    LavaJobTestResult,
)
from testrunner.forms import ResultComparisonForm


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
    jenkins_builds = jenkins_job.builds.filter(is_umbrella=False).order_by("-timestamp")[:10]
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

@login_required
def compare_results(request):
    if request.method == "POST":
        form = ResultComparisonForm(request.POST)
        if form.is_valid():
            testsets = form.cleaned_data['testresults']
            testcase_names = LavaJobTestResult.objects.filter(
                lava_job_result__in=testsets).order_by("test_case_id").values("test_case_id").distinct("test_case_id")
            testcase_list = []
            for testcase in testcase_names:
                tc_id = testcase['test_case_id']
                testcase_list.append({'name': tc_id, 'results': [], 'is_different': False})
                for testset in testsets:
                    result = testset.lavajobtestresult_set.filter(test_case_id=tc_id)
                    if result:
                        testcase_list[-1]['results'].append(result[0].status.name) # there should be only one?
                    else:
                        testcase_list[-1]['results'].append("Missing")
                if len(set(testcase_list[-1]['results'])) > 1:
                    testcase_list[-1]['is_different'] = True

            template = loader.get_template('testrunner/compare_results.html')
            context = RequestContext(request, {
                'testsets': testsets,
                'testcases': testcase_list,
            })
            return HttpResponse(template.render(context))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
