#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',



    #Direct URLs ------------------------------------

    url(r'^add/(?P<enumeration_id>\S+)',
                    add_direct_address, name="add_direct_address"),

    url(r'^delete/(?P<direct_id>\S+)/(?P<enumeration_id>\S+)',
                    delete_direct_address, name="delete_direct_address"),

    )
