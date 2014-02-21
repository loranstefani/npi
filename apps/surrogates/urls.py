#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   
    #surrogate URLs ------------------------------------
    
    url(r'^grant-management/(?P<key>\S+)',
                    grant_management, name="surrogate_grant_management"),

    )
