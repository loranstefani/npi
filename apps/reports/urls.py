#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    
    url(r'provider-enumeration-stats-by-state$',
                enumerations_stats_by_state,
                name = "enumeration_stats_by_state"),


    url(r'search$',
                reports_search,
                name = "reports_search"),

    url(r'enumerated-applications$',
                enumerated_applications,
                name = "enumerated_applications"),
    
    url(r'event-totals$',
                event_totals,
                name = "event_totals"),

    url(r'enumerated-applications$',
                enumerated_applications,
                name = "enumerated_applications"),
    
    url(r'view-errors/(?P<enumeration_id>\S+)$', view_errors, name = "reports_view_errors"),
    url(r'view-events/(?P<enumeration_id>\S+)$', view_events, name = "reports_view_events"),
    
    url(r'rescan-for-errors/(?P<enumeration_id>\S+)$', rescan_for_errors, name = "reports_rescan_for_errors"),

    
    url(r'application-overview$',
                application_overview,
                name = "application_overview"),

    url(r'staff-member-summary/(?P<username>\S+)/(?P<date_start>\S+)/(?P<date_stop>\S+)',
        staff_member_summary,
                name = "staff_member_summary"),

    url(r'pending-applications$',
                pending_applications,
                name = "pending_applications"),
        
    url(r'$', report_index, name="report_index"),
    
    )
