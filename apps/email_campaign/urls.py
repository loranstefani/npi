#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    
    url(r'sns-email-bounce$', sns_email_bounce, name = "sns_email_bounce"),
    url(r'sns-email-complaint$', sns_email_complaint, name = "sns_email_complaint"),
    
    )