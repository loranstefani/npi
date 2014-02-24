#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   
    #surrogate URLs ------------------------------------
    
    url(r'^grant-management-enumeration/(?P<key>\S+)',
                    grant_management_enumeration, name="surrogate_grant_management_enumeration"),
    
    url(r'^grant-management-ein/(?P<key>\S+)',
                    grant_management_ein, name="surrogate_grant_management_ein"),

    )
