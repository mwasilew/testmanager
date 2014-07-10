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

from django.core.management.base import BaseCommand
from django.conf import settings
from testmanager.testrunner.models import Bug
from helpers.jenkins_lava import fetch_jenkins_builds
from helpers.bugtracker import BugTracker

log = logging.getLogger('testrunner')


class Command(BaseCommand):
    def handle(self, *args, **options):
        log.setLevel(logging.DEBUG)
        for tracker in settings.TRACKERS:
            tracker_buglist = Bug.objects.filter(tracker=tracker).values_list('alias', flat=True)
            bugtracker = BugTracker(tracker, settings.TRACKERS[tracker])
            bugtracker.update_bugs(tracker_buglist)
