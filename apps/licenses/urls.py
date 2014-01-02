#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   


    #Address URLs ------------------------------------
    
    url(r'^add/(?P<enumeration_id>\S+)',
                    add_license, name="add_license"),


    url(r'^delete/(?P<license_id>\S+)/(?P<enumeration_id>\S+)',
                    delete_license, name="delete_license"),


    url(r'^manual-add/(?P<enumeration_id>\S+)',
                    manual_add_license, name="manual_add_license"),

    )
