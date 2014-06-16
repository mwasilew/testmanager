from django.conf.urls import patterns, url, include
from testrunner.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^jenkins_job/(?P<job_name>[0-9a-zA-Z_\-]+)$', jenkins_job_view, name='jenkins_job_view'),
                       #url(r'^jenkins_job/build/(?P<build_name>[a-zA-Z_\-]+)', jenkins_build_list, name='jenkins_build_list'),
                       url(r'^jenkins_job/(?P<job_name>[0-9a-zA-Z_\-]+)/build/(?P<build_number>\d+)$', jenkins_build_view, name='jenkins_build_view'),
                       url(r'^jenkins_job/(?P<job_name>[0-9a-zA-Z_\-]+)/build/(?P<build_number>\d+)/(?P<lava_job_number>\d+)$', lava_job_view, name='lava_job_view'),

                       # compare test results
                       url(r'^compare_results/$', compare_results, name='compare_results'),
              )
