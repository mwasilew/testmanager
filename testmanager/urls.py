from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testplanner.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'testdashboard.views.default'),
    (r'^testrunner/',
        include('testrunner.urls', app_name="testrunner")),
    (r'^testplanner/',
        include('testplanner.urls', app_name="testplanner")),

    url(r'^admin/', include(admin.site.urls)),

    # Login
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
     {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/'}),

)
