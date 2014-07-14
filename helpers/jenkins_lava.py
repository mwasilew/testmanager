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

import re
import ast
import json
import logging
import requests
import traceback
import xmlrpclib
from requests.exceptions import ConnectionError
#from urllib2 import URLError
from datetime import datetime
from django.conf import settings
from testmanager.testplanner.models import (
    Device,
    TestDefinition,
    TestDefinitionRevision
)
from testmanager.testrunner.models import (
    JenkinsJob,
    JenkinsBuild,
    JenkinsBuildStatus,
    LavaJob,
    LavaJobStatus,
    LavaJobResult,
    LavaJobResultStatus,
    LavaJobTestResult,
    LavaJobTestResultUnit
)

RUNNING = "RUNNING"
ERROR = "ERROR"
log = logging.getLogger('testrunner')


class LavaServerException(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return repr(self.name)


class LavaServer(object):

    def __init__(self, lava_url, username, token):
        self.lava_url = lava_url
        self.username = username
        self.token = token

    def call_xmlrpc(self, method_name, *method_params):
        payload = xmlrpclib.dumps((method_params), method_name)

        response = requests.request('POST', self.lava_url,
                                    data = payload,
                                    headers = {'Content-Type': 'application/xml'},
                                    auth = (self.username, self.token),
                                    timeout = 100,
                                    stream = False)

        if response.status_code == 200:
            result = xmlrpclib.loads(response.content)[0][0]
            return result
        else:
            raise LavaServerException(response.status_code)


def fetch_jenkins_builds(jenkins_db_job, jenkins_job, jenkins_build):
    lava_server = LavaServer(
         settings.LAVA_SERVER_URL,
         settings.LAVA_SERVER_USERNAME,
         settings.LAVA_SERVER_TOKEN)

    lava_job_regexp = re.compile(settings.LAVA_JOB_ID_REGEXP)
    build = None
    try:
        build = jenkins_job.get_build(jenkins_build)
    except ConnectionError:
        logger.error("ConnectionError when fetchin Jenkins build: {0}".format(jenkins_build))
        return
    # create umbrella build in DB
    db_build = create_jenkins_build(build, jenkins_db_job)
    log.debug("master build: {0} {1}".format(db_build.number, db_build.name))
    is_matrix = False
    log.debug("fetching matrix builds")
    try:
        for run in build.get_matrix_runs():
            is_matrix = True
            # mitigate Jenkins API bug. Sometimes API contains old builds
            if db_build.number == run.get_number():
                db_run = create_jenkins_build(run, jenkins_db_job, False, db_build)
                if db_run:
                    if 'description' in run._data and run._data['description']:
                        log.debug("Jenkins build description: {0}".format(run._data['description']))
                        for r in lava_job_regexp.finditer(run._data['description']):
                            log.debug('LAVA job ID: {0}'.format(r.group('lava_job_id')))
                            get_lava_job_details(r.group('lava_job_id'), db_run, lava_server)
                    else:
                        log.debug("no description for build")
                        for r in lava_job_regexp.finditer(run.get_console()):
                            log.debug('LAVA job ID: {0}'.format(r.group('lava_job_id')))
                            get_lava_job_details(r.group('lava_job_id'), db_run, lava_server)
            else:
                log.warning(
                    "Matrix build run {0} comes from other master build".format(
                        run.get_number()))
        if not is_matrix:
            db_run = create_jenkins_build(build, jenkins_db_job, False, db_build)
            if db_run:
                if 'description' in build._data and build._data['description']:
                    log.debug("Jenkins build description: {0}".format(build._data['description']))
                    for r in lava_job_regexp.finditer(build._data['description']):
                        get_lava_job_details(r.group('lava_job_id'), db_run, lava_server)
    except ConnectionError:
        log.error("ConnectionError occured. Probably timeout")
        log.error(traceback.print_exc())
        build_status, created = JenkinsBuildStatus.objects.get_or_create(name = ERROR)
        db_build.status = build_status
        db_build.save()


def get_lava_job_details(job_id, jenkins_build, lava_server=None):
    if lava_server is None:
        lava_server = LavaServer(
             settings.LAVA_SERVER_URL,
             settings.LAVA_SERVER_USERNAME,
             settings.LAVA_SERVER_TOKEN)

    try:
        try:
            job_details = lava_server.call_xmlrpc("scheduler.job_details", job_id)
        except LavaServerException:
            return False, "Lava Server Connection Problem"
        
        db_device = None
        if 'requested_device_type_id' in job_details and job_details['requested_device_type_id']:
            db_device, created = Device.objects.get_or_create(
                name = job_details['requested_device_type_id'])
        else:
            # try to decode the device type from the device name
            # it is assumed that device ID ends with 2 digit number added to device type
            db_device, created = Device.objects.get_or_create(name = job_details['actual_device_id'][0:-2])
        job_status = lava_server.call_xmlrpc("scheduler.job_status", job_id)
        #print 'LAVA job status:', job_status['job_status']
        lava_db_job_status, created = LavaJobStatus.objects.get_or_create(name = job_status['job_status'])
        lava_job_defaults = {
            'status': lava_db_job_status,
            'device_type': db_device
        }
        #lava_db_job = LavaJob(
        #    jenkins_build = jenkins_build,
        #    number = job_details['id'],
        #    status = lava_db_job_status,
        #
        #    )
        lava_db_job, lava_db_job_created = LavaJob.objects.get_or_create(
            jenkins_build = jenkins_build,
            number = job_details['id'],
            defaults = lava_job_defaults)
        # make sure the fields are updated if the job object already exists
        if not lava_db_job_created:
            lava_db_job.status = lava_db_job_status
            lava_db_job.device_type = db_device
            lava_db_job.save()
        log.debug(db_device)
        #if db_device:
        #    log.debug("adding db_device {0} to lava job {1}".format(db_device, lava_db_job))
        #    lava_db_job.device_type = db_device

        lava_db_job.submit_time = datetime.strptime(str(job_details['submit_time']), '%Y%m%dT%H:%M:%S')
        if 'start_time' in job_details and job_details['start_time']:
            log.debug("Start time: {0}".format(job_details['start_time']))
            lava_db_job.start_time = datetime.strptime(str(job_details['start_time']), '%Y%m%dT%H:%M:%S')

        job_definition = ast.literal_eval(job_details['definition'].replace("\n","").replace(" ","").replace("false","False"))

        job_definition_tests = []
        for action in job_definition['actions']:
            if action['command'] == "lava_test_shell":
                # ignore lava_android_test_run as these are not in db yet
                #or action['command'] == "lava_android_test_run":
                job_definition_tests += action['parameters']['testdef_repos']

        #lava_db_job.save()
        #print "Test runs scheduled", len(job_definition_tests)
        for test_def in job_definition_tests:
            # find test definition object
            log.debug("adding test definition {0} from repository {1} to LAVA {2}".format(test_def['testdef'], test_def['git-repo'], lava_db_job))
            db_test_def_list = TestDefinition.objects.filter(
                test_file_name = test_def['testdef'],
                repository__url = test_def['git-repo'])
            if db_test_def_list:
                # attach first test in the list to lava job
                lava_db_job.test_definitions.add(db_test_def_list[0])
        lava_db_job.save()

        if 'bundle_sha1' in job_status and job_status['bundle_sha1']:
            bundle_hash = job_status['bundle_sha1']
            bundle = json.loads(lava_server.call_xmlrpc("dashboard.get", bundle_hash)['content'])
            log.debug("Test runs executed: {0}".format(len(bundle['test_runs'])))
            for run in iter(bundle['test_runs']):
                if run['test_id'] != 'lava':
                    # find test definition corresponding to the results
                    # lava should not execute test that wasn't requested
                    log.debug("trying to find test definition with ID: {0} from LAVA {1}".format(run['test_id'], lava_db_job))
                    # test_id is not unique, but there is no better way of matching results to definition at this point
                    result_test_definition = lava_db_job.test_definitions.filter(test_id = run['test_id'])
                    log.debug(run['test_id'])
                    lava_db_result = LavaJobResult(
                        lava_job = lava_db_job
                    )
                    if result_test_definition:
                        result_test_definition = result_test_definition[0]
                        lava_db_result.test_definition = result_test_definition
                    if 'testdef_metadata' in run and result_test_definition:
                        # check if there is a corresponding version in db
                        test_definition_revision_list = result_test_definition.testdefinitionrevision_set.filter(revision = run['testdef_metadata']['version'])
                        if test_definition_revision_list:
                            log.debug("assigning test definition revision with sha1: {0}".format(test_definition_revision_list[0]))
                            lava_db_result.test_revision = test_definition_revision_list[0]

                    lava_db_result.save()
                    for test_result in iter(run['test_results']):
                        log.debug("trying to save test results {0}".format(test_result['test_case_id']))
                        test_result_status, created = LavaJobResultStatus.objects.get_or_create(name = test_result['result'])
                        lava_db_test_result = LavaJobTestResult(
                            lava_job_result = lava_db_result,
                            status = test_result_status,
                            test_case_id = test_result['test_case_id']
                            )
                        if 'measurement' in test_result:
                            db_unit, created = LavaJobTestResultUnit.objects.get_or_create(name = test_result['units'])
                            lava_db_test_result.is_measurement = True
                            lava_db_test_result.value = test_result['measurement']
                            lava_db_test_result.unit = db_unit
                        lava_db_test_result.save()
        return True, ""
    except ConnectionError:
        error = "URLError occured. Probably timeout"
        log.error("URLError occured. Probably timeout")
        log.error(traceback.print_exc())
        build_status, created = JenkinsBuildStatus.objects.get_or_create(name = ERROR)
        jenkins_build.status = build_status
        jenkins_build.save()

        return False, error

def create_jenkins_build(jenkins_build, jenkins_db_job, is_umbrella = True, umbrella_db_build = None):
    status_name = RUNNING
    try:
        if not jenkins_build.is_running():
            status_name = jenkins_build.get_status()
        build_status, created = JenkinsBuildStatus.objects.get_or_create(name = status_name)
        jenkins_build_defaults = {
            "status": build_status,
            "is_umbrella": is_umbrella,
            "timestamp": jenkins_build.get_timestamp()
        }
        db_build, db_build_created = JenkinsBuild.objects.get_or_create(
            name = jenkins_build.name,
            job = jenkins_db_job,
            number = jenkins_build.get_number(),
            defaults = jenkins_build_defaults
            )
        if not is_umbrella and umbrella_db_build:
            db_build.umbrella_build = umbrella_db_build
        if not db_build_created:
            db_build.status = build_status
            db_build.is_umbrella = is_umbrella
            db_build.timestamp = jenkins_build.get_timestamp()
        db_build.save()
        if db_build_created:
            #log.debug("Jenkins build {0} created ({1})".format(jenkins_build.get_number(), jenkins_build.name.decode('ascii', 'ignore')))
            log.debug("Jenkins build {0} created ({1})".format(jenkins_build.get_number(), ''.join([x for x in jenkins_build.name if ord(x) < 128])))
        else:
            #log.debug("Jenkins build {0} updated ({1})".format(jenkins_build.get_number(), jenkins_build.name.decode('ascii', 'ignore')))
            log.debug("Jenkins build {0} updated ({1})".format(jenkins_build.get_number(), ''.join([x for x in jenkins_build.name if ord(x) < 128])))
        return db_build
    except ConnectionError:
        log.debug("Connection error on build: {0}".format(''.join([x for x in jenkins_build.name if ord(x) < 128])))
        build_status, created = JenkinsBuildStatus.objects.get_or_create(name = status_name)
        if umbrella_db_build:
            umbrella_db_build.status = build_status
            umbrella_db_build.save()
