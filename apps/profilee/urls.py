#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    url(r'random$', display_random_enumeration_profile, name="display_random_enumeration_profile"),
    url(r'npi/(?P<number>\w+).json$', display_enumeration_profile_json, name="display_enumeration_profile_json"),

    url(r'npi/(?P<number>\S+)$', display_enumeration_profile, name="display_enumeration_profile"),
    
    
    
    url(r'id/(?P<enumeration_id>\S+)$', display_enumeration_profile_by_id, name="display_enumeration_profile_by_id"),
    )
