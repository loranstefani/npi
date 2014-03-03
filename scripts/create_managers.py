#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import sys, csv
from django.conf import settings
import datetime
from apps.enumerations.models import Enumeration
from apps.surrogates.models import Surrogate
from django.contrib.auth.models import User



def create_managers():
    
    users = User.objects.all()
    
    for u in users:
        s = Surrogate.objects.get_or_create(user=u)
        enums = Enumeration.objects.all()[:10]
        for e in enums:
            s.enumerations.add(e)
            e.managers.add(u)
   
    print "Done."
            
def run():

    try:
        create_managers()
    except:
        print "Error."
        print sys.exc_info()
