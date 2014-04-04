from django.conf.urls.defaults import *
from testrunner.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^jenkins_job/(?P<job_name>[a-zA-Z_\-]+)$', jenkins_job_view, name='jenkins_job_view'),
                       #url(r'^jenkins_job/build/(?P<build_name>[a-zA-Z_\-]+)', jenkins_build_list, name='jenkins_build_list'),
                       url(r'^jenkins_job/(?P<job_name>[a-zA-Z_\-]+)/build/(?P<build_number>\d+)$', jenkins_build_view, name='jenkins_build_view'),
              )
