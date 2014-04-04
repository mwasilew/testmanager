from django.conf.urls.defaults import *
from testplanner.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^new$', testplan_new, name='testplan_new'),
              )
