#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *
from django.views.generic import TemplateView


urlpatterns = patterns('',
   
    url(r'public-data$',   TemplateView.as_view(template_name='public-data.html'),
                            name='public_data_download'),
    
    url(r'api-documentation$',   TemplateView.as_view(template_name='api-documentation.html'),
                            name='api_documentation'),
    )
