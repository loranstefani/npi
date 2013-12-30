#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   


    #Address URLs ------------------------------------
    
    url(r'^add/(?P<enumeration_id>\S+)',
                    add_license, name="add_license"),


    )
