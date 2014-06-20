#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings 
from django.http import Http404
import uuid, re, json
from collections import OrderedDict

def get_enumeration_user_manages_or_404(Enumeration, enumeration_id, user):
    """
    Make sure the user has the right to mange this enumeration.
    Returns the enumeration object or raises 404.
    """
    
    #if user.is_staff==False:
    try:
        e = Enumeration.objects.select_related('managers').get(id=enumeration_id,
                                                               managers=user)
        return e
 
    except Enumeration.DoesNotExist:
        raise Http404('Not Found.')
    
    ##Else this is a staff user so let he or she continue.
    ##else
    #    try:
    #        e = Enumeration.objects.get(id=enumeration_id)
    #        return e
    # 
    #    except Enumeration.DoesNotExist:
    #        raise Http404('Not Found.')      



def valid_uuid(uuid):
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(str(uuid))
    return bool(match)
    
def generate_provider_json(e):
    """e is an enumeration model instance"""
    d     = OrderedDict()
    basic = OrderedDict()
     
    d['enumeration_type']      = e.enumeration_type
    d['number']                = e.number, 
    d['basic']                 = None
    d['addresses']             = []
    d['taxonomies']            = []
    d['licenses']              = []
    d['identifiers']           = []
    basic['authorized_official_credential']= e.authorized_official_credential
    #'authorized_official_email',
    #'authorized_official_first_name',
    #'authorized_official_last_name',
    #'authorized_official_middle_name',
    #'authorized_official_prefix',
    #'authorized_official_suffix',
    #'authorized_official_telephone_extension',
    #'authorized_official_telephone_number',
    #'authorized_official_title',
    #'authorized_official_title_or_position',
    #'bio_headline',
    #'classification',
    #'comments',
    #'confirmation',
    #'contact_method',
    #'contact_person_credential',
    #'contact_person_email',
    #'contact_person_first_name',
    #'contact_person_last_name',
    #'contact_person_middle_name',
    #'contact_person_prefix',
    #'contact_person_suffix',
    #'contact_person_telephone_extension',
    #'contact_person_telephone_number',
    #'contact_person_title',
    #'contact_person_title_or_position',
    #'correspondence_address',
    #'country_of_birth',
    #'credential',
    #'date_of_birth',
    #'date_of_death',
    #'deactivated_details',
    #'deactivation_date',
    #'deactivation_reason_code',
    #'decativation_note',
    #'deceased_fuzzy_match',
    #'deceased_in_dmf',
    #'deceased_notes',
    #'deceased_notice_day_sent',
    #'direct_addresses',
    #'direct_certificates',
    #'dmf_incorrect',
    #'doing_business_as',
    #'driving_directions',
    #'ein',
    #'ein_image',
    #'enumerated_by',
    #'enumeration_date',
    #'enumeration_parent_organization',
    #'enumeration_type',
    #'event',
    #'facebook_handle',
    #'first_name', 'gender', 'identifiers',
    #'initial_enumeration_date',
    #'itin',
    #'last_name',
    #'last_updated',
    #'location_address',
    #'mailing_address',
    #'managers',
    #'medical_record_storage_address',
    #'middle_name',
    #'mode',
    #'name_prefix',
    #'name_suffix',
    #'number', 'old_numbers', 'organization_name',
    #'organization_other_name', 'organization_other_name_code',
    #'organizational_subpart', 'other_addresses', 'other_first_name_1',
    #'other_first_name_2', 'other_last_name_1', 'other_last_name_2',
    #'other_middle_name_1', 'other_middle_name_2', 'other_name_code_1',
    #'other_name_code_2', 'other_name_credential_1',
    #'other_name_credential_2', 'other_name_prefix_1',
    #'other_name_prefix_2', 'other_name_suffix_1',
    #'other_name_suffix_2', 'other_taxonomies',
    #'parent_organization', 'parent_organization_ein',
    #'parent_organization_legal_business_name',
    #'pecos_id', 'pii_lock',
    #'public_email',
    #'reactivation_date',
    #'recativation_note',
    #'replacement_npi',
    #'revalidation_address',
    #'sole_proprietor',
    #'specialties',
    #'specialty',
    #'ssn',
    #'state_of_birth',
    #'status',
    #'taxonomy',
    #'updated',
    #'website'
    
    d['basic'] = basic
    
    return json.dumps(d, indent = 4)
    