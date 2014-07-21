#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
    
    
    #Administrative URLs -----------------------------
    url(r'^history/(?P<enumeration_id>\S+)',
                    create_historical_report, name="enmeration_create_historical_report"),
    

    #Taxonomy URLs -----------------------------------
    url(r'^taxonomy/(?P<enumeration_id>\S+)',
                    primary_taxonomy, name="primary_taxonomy"),

    url(r'^add-other-taxonomies/(?P<enumeration_id>\S+)',
                    add_other_taxonomies, name="add_other_taxonomies"),


    url(r'^delete-other-taxonomy/(?P<taxonomy_id>\S+)/(?P<enumeration_id>\S+)',
                    delete_other_taxonomy, name="delete_other_taxonomy"),

    #Specialty URLs
    url(r'^specialty/(?P<enumeration_id>\S+)',
                    primary_specialty, name="primary_specialty"),

    #Address URLs ------------------------------------


    url(r'^address/delete/(?P<address_id>\S+)/(?P<enumeration_id>\S+)',
                    delete_address, name="delete_address"),

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

    url(r'^ein-lookup$', ein_lookup, name="ein_lookup"),
    url(r'^self-take-over', self_take_over, name="enmeration_self_take_over"),

    url(r'^request-to-manage-enumeration/(?P<id>\S+)$',
                            request_to_manage_enumeration,
                            name="request_to_manage_enumeration"),


    url(r'^request-to-manage-ein/(?P<ein>\S+)$',request_to_manage_ein,
                            name="request_to_manage_ein"),

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

    url(r'^edit-pii/(?P<id>\S+)', edit_pii,
                    name="edit_pii_enumeration"),


    url(r'^contact-person/(?P<id>\S+)$', contact_person, name="contact_person"),

    url(r'^authorized-official/(?P<id>\S+)', authorized_official,
                    name="authorized_official"),

    url(r'^other-names/(?P<id>\S+)', other_names, name="other_names"),


    url(r'^edit-enhanced/(?P<id>\S+)', edit_enhanced_enumeration,
                    name="edit_enhanced_enumeration"),

    url(r'^stop-managing/(?P<enumeration_id>\S+)$', stop_managing_enumeration,
                    name="stop_managing_enumeration"),

    url(r'^edit/(?P<id>\S+)', edit_enumeration, name="edit_enumeration"),
    
    url(r'^flag-for-deactivation/(?P<id>\S+)', flag_for_deactivation,
                    name="flag_for_deactivation"),
    
    url(r'^flag-for-fraud/(?P<id>\S+)', flag_for_fraud, name="flag_for_fraud"),

    url(r'^activate/(?P<id>\S+)', activate, name="enumeration_activate"),
    url(r'^deactivate/(?P<id>\S+)', deactivate, name="enumeration_deactivate"),
    url(r'^reject/(?P<id>\S+)', reject, name="enumeration_reject"),
    url(r'^reactivate/(?P<id>\S+)', reactivate, name="enumeration_reactivate"),
    url(r'^replace/(?P<id>\S+)', replace, name="enumeration_replace"),
    url(r'^submit-dialouge/(?P<id>\S+)', submit_dialouge, name="enumeration_submit_dialouge"),

    url(r'^events/resend-mail/(?P<event_id>\S+)', resend_mail, name="enumeration_event_resend_mail"),
    url(r'^events/resend-email/(?P<event_id>\S+)', resend_email, name="enumeration_event_resend_email"),

    )
