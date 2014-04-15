import logging
from django.conf import settings
from django.core.management.base import (
    BaseCommand, 
    CommandError
)
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
