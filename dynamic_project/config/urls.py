from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.auto.views import HomeView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ensure_csrf_cookie(HomeView.as_view()), name="home"),
    url(r'^api/', include('apps.auto.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
