#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   


    #Address URLs ------------------------------------
    
    url(r'^address/edit/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    edit_address, name="edit_address"),

    url(r'^address/select-address-type/(?P<enumeration_id>\S+)', select_address_type,
                    name="select_address_type"),
    
    url(r'^address/domestic-address/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    domestic_address, name="domestic_address"),    
    
    url(r'^address/foreign-address/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    foreign_address, name="foreign_address"),
    
    url(r'^address/military-address/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    military_address, name="military_address"),
    
    
    
    #Enumeration URLs -------------------------------------
    url(r'^create/$', create_enumeration,
                    name="create_enumeration"),
    
    url(r'^create-individual/(?P<id>\S+)', create_individual_enumeration,
                    name="create_individual_enumeration"),
    
    url(r'^create-organization/(?P<id>\S+)', create_organization_enumeration,
                    name="create_organization_enumeration"),

    url(r'^stop-managing/(?P<enumeration_id>\S+)', stop_managing_enumeration,
        name="stop_managing_enumeration"),

    url(r'^edit/(?P<id>\S+)', edit_enumeration,
                    name="edit_enumeration"),
    
    

    )
