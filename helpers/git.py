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

import os
import traceback
import logging
import yaml
from django.db.models import ManyToManyField
from testmanager.testplanner.models import (
#    TestRepository,
    Maintainer,
    OS,
    Scope,
    Device,
    TestDefinition,
    TestDefinitionRevision
)

log = logging.getLogger('testplanner')

def extract_metadata(metadata, field_name, object_class, meta_attribute='name'):
    meta_list = []
    if field_name in metadata and metadata[field_name]:
        for field_value in metadata[field_name]:
            newobject, created = object_class.objects.get_or_create(**{meta_attribute:field_value})
            meta_list.append(newobject)
    return meta_list

def create_from_yaml(tc, blob, commit, repository):
    try:
        test_id = tc['metadata']['name']
        test_name = tc['metadata']['name'] + "@" + blob.path.rstrip(blob.name).rstrip("/")
        test_file_name = blob.path
        test_description = tc['metadata']['description']
        test_defaults = {
            'repository': repository,
            'test_file_name': test_file_name,
            'description': test_description,
        }
        newtest, created = TestDefinition.objects.get_or_create(
            name=test_name,
            test_id=test_id,
            defaults=test_defaults)
        tc_maintainer_list = extract_metadata(tc['metadata'], 'maintainer', Maintainer, 'email')
        test_defaults.update({'maintainer': tc_maintainer_list})

        tc_os_list = extract_metadata(tc['metadata'], 'os', OS)
        test_defaults.update({'os': tc_os_list})

        tc_scope_list = extract_metadata(tc['metadata'], 'scope', Scope)
        test_defaults.update({'scope': tc_scope_list})

        tc_device_list = extract_metadata(tc['metadata'], 'devices', Device)
        test_defaults.update({'device': tc_device_list})
        
        if 'environment' in tc['metadata'] and \
           'manual-test' in tc['metadata']['environment'] and \
           tc['metadata']['format'].startswith('Manual'):
            newtest.is_automated = False

        if not created:
            for attr, value in test_defaults.iteritems():
                attribute = getattr(newtest, attr)
                if isinstance(newtest._meta.get_field_by_name(attr)[0],
                              ManyToManyField):
                    if set([x.pk for x in attribute.all()]) != set(value):
                        log.debug("{0} old: {1}, new: {2}".format(
                            attr, [x.pk for x in attribute.all()], value))
                        setattr(newtest, attr, value)
                else:
                    if attribute != value:
                        log.debug("{0} old: {1}, new: {2}".format(
                            attr, getattr(newtest, attr), value))
                        setattr(newtest, attr, value)
        else:
            newtest.maintainer = tc_maintainer_list
            newtest.os = tc_os_list
            newtest.scope = tc_scope_list
            newtest.device = tc_device_list
        newtest.save()
        revision, created = TestDefinitionRevision.objects.get_or_create(revision=commit.hexsha)
        if newtest not in revision.test_definition.all():
            revision.test_definition.add(newtest)
    except:
        log.error("problem with {0} and {1}".format(commit.hexsha, blob.name))
        traceback.print_exc()

def copy_commits_to_db(r, repository, lastsha=None):
    commit_search = "HEAD"
    if lastsha:
        commit_search = "%s..HEAD" % lastsha
    for commit in r.iter_commits(commit_search, max_count=100, reverse=True):
        for blob in commit.tree.list_traverse():
            print blob.path, blob.name
            # process only yaml files
            # ignore symlinks
            if blob.name.endswith("yaml"):
                try:
                    if blob.mode == blob.file_mode:
                        tc = yaml.load(blob.data_stream.read())
                        create_from_yaml(tc, blob, commit, repository)
                    if blob.mode == blob.link_mode:
                        os.chdir(os.path.dirname(blob.abspath))
                        realfile = open(blob.data_stream.read(), 'r')
                        tc = yaml.load(realfile)
                        realfile.close()
                        create_from_yaml(tc, blob, commit, repository)
                except yaml.YAMLError:
                    pass

        log.info("updated head revision to: {0}".format(commit.hexsha))
        repository.head_revision = commit.hexsha
        repository.save()
