from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.auto.views import HomeView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^api/', include('apps.auto.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
