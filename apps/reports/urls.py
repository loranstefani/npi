#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    
    url(r'provider-enumeration-stats-by-state$',
                enumerations_stats_by_state,
                name = "enumeration_stats_by_state"),
    
    url(r'pending-applications$',
                pending_applications,
                name = "pending_applications"),
    
    url(r'$', report_index, name="report_index"),
    
    )
