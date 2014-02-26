#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    url(r'random$', display_random_enumeration_profile, name="display_random_enumeration_profile"),
    url(r'(?P<number>\S+)$', display_enumeration_profile, name="display_enumeration_profile"),
    )
