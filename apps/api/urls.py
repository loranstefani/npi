#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',

    #VIEW -----------------------------------
    url(r'^enumeration/view/(?P<enumeration_number>\S+)',
                    api_view_enumeration, name="api_view_enumeration"),
    #UPDATE
    url(r'^enumeration/update',
                    api_enumeration_update, name="api_enumeration_update"),

    #CREATE
    url(r'^enumeration/create',
                    api_enumeration_create, name="api_enumeration_create"),

    )
