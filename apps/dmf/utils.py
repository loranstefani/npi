#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
import datetime
from apps.enumerations.models import Enumeration, Event
from apps.enumerations.notifications import DECEASED_SUBJECT, DECEASED_BODY



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
        first_name = line[34:49] 
        last_name  = line[10:34]
        date_death =  line[65:73]

        try:
            # Do we have any matching decased individuals in our Enumeration model?
            # If already marked
            e = Enumeration.objects.get(ssn = ssn, deceased_in_dmf = False)
            #Only do a check if first and last names are given(this should always be True)
            if e.last_name and e.last_name:
                if str(e.last_name[0]) == str(last_name[0]) and \
                   str(e.first_name[0]) == str(first_name[0]):
                    #appears to be the same person
                    e.deceased_in_dmf = True
                    
                    #deactivate Enumeration
                    e.status = "D"
                    note = "%s %s died on %s" % (first_name, last_name, date_death)
                    #Create an event                      
                    Event.objects.create(enumeration=e,
                                        event_type="DEACTIVATED-DECEASED",
                                        note= note,
                                        body =  DECEASED_BODY,
                                        subject = DECSEAED_SUBJECT
                                        )
                    
                else:
                    #The SSN matched but the name did not. This is a fuzzy match
                    # and should be evaluated by a human. 
                    e.deceased_fuzzy_match =True
                    
                    note = "Fuzzy: %s %s with SSN %s died on %s." % (first_name,
                                                                     last_name,
                                                                     ssn, date_death)
                    
                    Event.objects.create(enumeration=e, event_type="FUZZY-DECEASED",
                                            send_now=False, note=note,
                                            body =  DECEASED_BODY,
                                            subject = DECSEAED_SUBJECT)

            e.date_of_death = datetime.date(int(date_death[4:8]),int(date_death[0:2]),int(date_death[2:4]))
            e.save()
            total += 1        
        except Enumeration.DoesNotExist:
            #The SSN is not attitubed to an Enumerations. 
            pass
            
        
    return total