#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    
    url(r'upload$', dmf_upload, name = "dmf_upload"),


  
    
    )