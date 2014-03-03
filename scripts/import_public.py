#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import sys, csv
from django.conf import settings
from datetime import datetime
from apps.enumerations.models import Enumeration
from apps.taxonomy.models import TaxonomyCode
from apps.addresses.models import Address
import resource


states = ("AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",)

military = ("APO","FPS", "DPO")



def import_public_corrected_addresses(filename):
    print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print "Opening", filename
    csvfile = csv.reader(open(filename, 'rb'), delimiter=',')
    print """Skiping the first header row. """
    next(csvfile)
    #next(csvfile)
    print "start file iteration"
    i=0
    for row in csvfile:
        i+=1 
        try:
            practice_address_1 ={}
            #if Enumeration.objects.filter(number=row[1]).count()==0:
            if True:    
                if i % 1000 == 0:
                    print i
                    print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    
                
                #Set the enumeration type
                if str(row[2])=="1":
                    enumeration_type = "NPI-1"
                elif  str(row[2])=="2":
                    enumeration_type = "NPI-2"
                
                
                #Fetch the updated practice addresses 
                practice_address_1   =row[17].upper()
                practice_address_2   =row[18].upper()
                practice_city        =row[19].upper()
                practice_state       =row[20].upper()
                practice_zip         =row[21].upper()
                practice_county_name =row[22].upper()
                practice_vacant      =row[23].upper()
                practice_active      =row[24].upper()
                practice_record_type =row[25].upper()
                practice_lat         =row[26].upper()
                practice_long        =row[27].upper()
                practice_rdi         =row[28].upper()
                
                if practice_state in states:
                    practice_address_type = "DOM"
                elif practice_state in military:
                    practice_address_type = "MIL"
                else:
                    practice_address_type = "FGN"
                
                #Fetch the updated mailing addresses 
                mailing_address_1    =row[37].upper()
                mailing_address_2   =row[38].upper()
                mailing_city        =row[39].upper()
                mailing_state       =row[40].upper()
                mailing_zip         =row[41].upper()
                mailing_county_name =row[42].upper()
                mailing_vacant      =row[43].upper()
                mailing_active      =row[44].upper()
                mailing_record_type =row[45].upper()
                mailing_lat         =row[46].upper()
                mailing_long        =row[47].upper()
                mailing_rdi         =row[48].upper()
                
                if mailing_state in states:
                    mailing_address_type = "DOM"
                elif mailing_state in military:
                    mailing_address_type = "MIL"
                else:
                    mailing_address_type = "FGN"
                
    
                location_address = Address.objects.create(address_1 = practice_address_1,
                                        address_2 = practice_address_2,
                                        city = practice_city,       
                                        state = practice_state,      
                                        zip = practice_zip,
                                        address_type = practice_address_type,
                                        address_purpose = "LOCATION",
                                        county_name  =   practice_county_name,
                                        vacant   =  practice_vacant,
                                        active    = practice_active,
                                        record_type =practice_record_type,
                                        lat        =practice_lat,
                                        long       =practice_long,
                                        rdi        =practice_rdi,)
                
                mailing_address = Address.objects.create(
                                        address_1       = mailing_address_1,
                                        address_2       = mailing_address_2,
                                        city            = mailing_city,       
                                        state           = mailing_state,      
                                        zip             = mailing_zip,
                                        address_type    = mailing_address_type,
                                        address_purpose = "MAILING",
                                        county_name     = mailing_county_name,
                                        vacant          = mailing_vacant,
                                        active          = mailing_active,
                                        record_type     = mailing_record_type,
                                        lat             = mailing_lat,
                                        long            = mailing_long,
                                        rdi             = mailing_rdi,)
                
                
                
                #The record doesn't exist so lets add it.
                e = Enumeration.objects.create(number=row[1],
                                               enumeration_type=enumeration_type,
                                               status="A",
                                               first_name = row[5].upper(),
                                               last_name = row[4].upper(),
                                               organization_name = row[3],
                                               location_address = location_address,
                                               mailing_address = mailing_address
                                               )

        except:
            print "last index was", i
            print "Error."
            print sys.exc_info()
            sys.exit(0)

    print "Completed",  i, "rows."
            
def run():

    import_public_corrected_addresses('scripts/npi_corrected_addresses.csv')
