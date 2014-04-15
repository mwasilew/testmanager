from django.conf.urls import patterns, url, include
from testplanner.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^new$', testplan_new, name='testplan_new'),
              )
