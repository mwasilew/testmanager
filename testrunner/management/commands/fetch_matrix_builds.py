import logging
import re

from django.conf import settings
#ToDo - get rid of lava_tool. Rewrite XML-RPC using token stored in settings
from lava_tool.authtoken import (
    AuthenticatingServerProxy, 
    KeyringAuthBackend
)
from django.core.management.base import (
    BaseCommand, 
    CommandError
)
from testrunner.models import JenkinsJob
from jenkinsapi.jenkins import Jenkins
from helpers.jenkins_lava import (
    get_lava_job_details,
    create_jenkins_build,
)

#log = logging.getLogger('testrunner.fetch_matrix_builds')
log = logging.getLogger('testrunner')


def fetch_jenkins_builds(jenkins_db_job, jenkins_job, lava_server, jenkins_build):
    lava_job_regexp = re.compile(settings.LAVA_JOB_ID_REGEXP)
    build = jenkins_job.get_build(jenkins_build)
    # create umbrella build in DB
    db_build = create_jenkins_build(build, jenkins_db_job)
    is_matrix = True
    for run in build.get_matrix_runs():
        log.debug("fetching matrix builds")
        is_matrix = False
        db_run = create_jenkins_build(run, jenkins_db_job, False, db_build)
        if 'description' in run._data and run._data['description']:
            log.debug("Jenkins build description: {0}".format(run._data['description']))
            r = lava_job_regexp.search(run._data['description'])
            if r:
                log.debug('LAVA job ID: {0}'.format(r.group('lava_job_id')))
                get_lava_job_details(lava_server, r.group('lava_job_id'), db_run)
    if not is_matrix:
        if 'description' in build._data and build._data['description']:
            log.debug("Jenkins build description: {0}".format(run._data['description']))
            r = lava_job_regexp.search(build._data['description'])
            if r:
                #print 'LAVA job ID:', r.group('lava_job_id')
                get_lava_job_details(lava_server, r.group('lava_job_id'), db_run)



class Command(BaseCommand):
    def handle(self, *args, **options):
        log.setLevel(logging.DEBUG)
        lava_server = AuthenticatingServerProxy(
            settings.LAVA_SERVER_URL,
            verbose=False,
            auth_backend=KeyringAuthBackend())
        #jenkins_device_regexp = re.compile(ur'%s\s\xc2\xbb\s(?P<device_name>\w+)' % (project), re.UNICODE)
        for job in JenkinsJob.objects.all():
            log.debug("processing {0}".format(job.name))
            jenkins = Jenkins(job.service.url)
            jenkins_job = jenkins[job.name]
            last_db_build = job.builds.filter(is_umbrella=True).order_by('-number')
            last_jenkins_build = jenkins_job.get_last_buildnumber()
            if last_db_build: 
                if last_db_build[0].number < last_jenkins_build:
                    for jenkins_build in range(last_db_build[0].number + 1, last_jenkins_build + 1):
                        fetch_jenkins_builds(job, jenkins_job, lava_server, jenkins_build)

            else: # no builds in db ?
                for jenkins_build in range(jenkins_job.get_first_buildnumber(), last_jenkins_build + 1):
                    fetch_jenkins_builds(job, jenkins_job, lava_server, jenkins_build)
