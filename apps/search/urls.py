#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *
from django.views.generic import TemplateView


urlpatterns = patterns('',
   
    url(r'^$',   search, name='search_npi'),


    )
