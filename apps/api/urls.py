#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

    #Write-----------------------------------
    url(r'^write',
                    api_enumeration_write, name="api_enumeration_write"),

    
    url(r'^events/since/(?P<date_start>\S+)',
                    events_since_date, name="api_events_since_date"),

    

    )
