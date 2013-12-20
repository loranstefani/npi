#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
   

    url(r'select-address-type/', select_address_type,
                       name="select_address_type"),
    
    url(r'domestic-address/(?P<id>\S+)', domestic_address,
                        name="domestic_address"),    
    
    url(r'foreign-address/(?P<id>\S+)', foreign_address,
                        name="foreign_address"),
    
    url(r'military-address/(?P<id>\S+)', military_address,
                        name="military_address"),    


    #url(r'create-domain-bound/(?P<serial_number>\S+)', create_domain_certificate,
    #                   name="create_domain_certificate"),
    #
    #
    #url(r'dashboard/', certificate_dashboard,
    #                   name="certificate_dashboard"),
    #
    #url(r'revoke-endpoint/(?P<serial_number>\S+)', revoke_domain_certificate,
    #                    name="revoke_domain_certificate"),    
    #
    #url(r'revoke-trust-anchor/(?P<serial_number>\S+)', revoke_trust_anchor_certificate,
    #                    name="revoke_trust_anchor_certificate"),    
    #
    )
