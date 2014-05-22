#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
import datetime
from apps.enumerations.models import Enumeration



def valid_dmf(f):
    # -1 indicates the file had an error. Defaults to error/
    result = True
    f.open(mode='rb')
    
    #sanity check the file by inspecting the first line.
    first_line = f.readline()
    try:
        ssn = first_line[1:10]
        ssn = int(ssn)
        date_death =  first_line[65:73]
        datetime.date(int(date_death[4:8]),int(date_death[0:2]),int(date_death[2:4]))
        result              
    except:
        result = False
    
    if len(first_line) not in [100,101,]:
         result = False
    f.close()
    return result


def process_dmf(f):
    
    # -1 indicates the file had an error. Defaults to error/
    total = -1
    
    
    f.open(mode='rb')
    #File seems legit so procss.
    total = 0
    #Go back to the start of the file.
    f.seek(0)
    lines = f.readlines()
    for line in lines:
        ssn = line[1:10]
        try:
            # Do we have any matching decased individuals in our Enumeration model?
            # If already marked
            e = Enumeration.objects.get(ssn = ssn, deceased_in_dmf = False)
            e.deceased_in_dmf = True
            date_death =  line[65:73]
            e.date_of_death = datetime.date(int(date_death[4:8]),int(date_death[0:2]),int(date_death[2:4]))
            e.save()
            total += 1        
        except Enumeration.DoesNotExist:
            #The SSN is not attitubed to an Enumerations. 
            pass
            
        
    return total