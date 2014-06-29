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

import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from helpers.git import copy_commits_to_db
from testplanner.models import TestRepository
from git import Repo

log = logging.getLogger('testplanner')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for repository in TestRepository.objects.filter(is_cloned=True):
            dirname = repository.url.split("/")[-1]
            local_repo_dir = "%s/%s" % (settings.REPOSITORIES_HOME, dirname)
            r = Repo(local_repo_dir)
            origin = r.remotes.origin
            origin.pull()
            copy_commits_to_db(r, repository, repository.head_revision)
