import logging
from django.core.management.base import (
    BaseCommand, 
    CommandError
)

log = logging.getLogger('testrunner')


class Command(BaseCommand):
    def handle(self, *args, **options):
