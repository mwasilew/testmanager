from django.conf.urls import url

from testmanager.testreporter import views


urlpatterns = [
    url(r'^$', views.Base.as_view()),
    url(r'^report/(?P<tag_id>[0-9]+)/$', views.Report_View.as_view()),
]
