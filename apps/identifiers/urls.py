#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   


    #Address URLs ------------------------------------
    
    url(r'^add/(?P<enumeration_id>\S+)',
                    add_identifier, name="add_identtifier"),

    url(r'^delete/(?P<identifier_id>\S+)/(?P<enumeration_id>\S+)',
                    delete_identifier, name="delete_identifier"),

    )
