#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   


    #Address URLs ------------------------------------
    
    url(r'^address/edit/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    edit_address, name="edit_address"),

    url(r'^address/select-address-type/(?P<address_purpose>\S+)/(?P<enumeration_id>\S+)',
                    select_address_type, name="select_address_type"),
    
    url(r'^address/domestic-address/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    domestic_address, name="domestic_address"),    
    
    url(r'^address/foreign-address/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    foreign_address, name="foreign_address"),
    
    url(r'^address/military-address/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    military_address, name="military_address"),
    
    
    
    #Enumeration URLs -------------------------------------
    
    url(r'^search$', search_enumeration, name="search_enumeration"),
    url(r'^surrogate-lookup$', surrogate_lookup, name="surrogate_lookup"),
    
    url(r'^request-to-manage/(?P<id>\S+)$',request_to_manage_enumeration,
                            name="request_to_manage_enumeration"),
    
    url(r'^create$', create_enumeration, name="create_enumeration"),
    
    url(r'^create-individual/(?P<id>\S+)', create_individual_enumeration,
                    name="create_individual_enumeration"),
    
    url(r'^create-organization/(?P<id>\S+)', create_organization_enumeration,
                    name="create_organization_enumeration"),
    
    
    url(r'^edit-individual/(?P<id>\S+)', create_individual_enumeration,
                    name="edit_individual_enumeration"),
    
    url(r'^edit-organization/(?P<id>\S+)', create_organization_enumeration,
                    name="edit_organization_enumeration"),
    
    url(r'^edit-basic/(?P<id>\S+)', edit_basic_enumeration,
                    name="edit_basic_enumeration"),

    url(r'^edit-enhanced/(?P<id>\S+)', edit_enhanced_enumeration,
                    name="edit_enhanced_enumeration"),

    url(r'^stop-managing/(?P<enumeration_id>\S+)', stop_managing_enumeration,
                    name="stop_managing_enumeration"),

    url(r'^edit/(?P<id>\S+)', edit_enumeration,
                    name="edit_enumeration"),
    


    
    

    )
