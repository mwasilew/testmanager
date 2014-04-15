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
        for repository in TestRepository.objects.all():
            if not repository.is_cloned:
                dirname = repository.url.split("/")[-1]
                local_repo_dir = "%s/%s" % (settings.REPOSITORIES_HOME, dirname)
                r = Repo.clone_from(repository.url, local_repo_dir)
                repository.local_dir = local_repo_dir
                repository.is_cloned = True
                repository.save()
                copy_commits_to_db(r, repository)
