#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *
from django.views.generic import TemplateView


urlpatterns = patterns('',
   
    url(r'^$',   TemplateView.as_view(template_name='statistics.html'),
                            name='statistics'),


    url(r'by-state$',   TemplateView.as_view(template_name='statistics.html'),
                            name='statistics_by_state'),

    )
