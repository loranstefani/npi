#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',



    #Taxonomy URLs ------------------------------------

    url(r'^add/(?P<enumeration_id>\S+)',
                    add_taxonomy, name="add_taxonomy"),

    url(r'^delete/(?P<taxonomy_id>\S+)/(?P<enumeration_id>\S+)',
                    delete_taxonomy, name="delete_taxonomy"),

    )
