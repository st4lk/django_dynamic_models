# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^(?P<model>[a-zA-z0-9_]+)/$',
        views.DynamicModelListCreateView.as_view(), name="dynamic_list"),
    url(r'^(?P<model>[a-zA-z0-9_]+)/(?P<pk>[0-9]+)/$',
        views.DynamicModelUpdateView.as_view(), name="dynamic_detail"),
)
