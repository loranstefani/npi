#!/usr/bin/env python
#-*- coding: utf-8 -*-
#vim: ai ts=4 sts=4 et sw=4
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
    d['number']                = e.number
    d['basic']                 = None
    d['addresses']             = []
    d['taxonomies']            = []
    d['specialties']           = []
    d['licenses']              = []
    d['identifiers']           = []
    d['direct_addresses']      = []
    
    
    # Build Up Basic
    
    # Name For individuals
    basic['name_prefix']= e.name_prefix
    basic['first_name']= e.first_name
    basic['last_name']= e.last_name
    basic['middle_name']= e.middle_name
    basic['name_suffix']= e.name_suffix
    basic['credential']  = e.credential
    basic['doing_business_as']= e.doing_business_as
    basic['sole_proprietor']= e.sole_proprietor
    basic['other_first_name_1']= e.other_first_name_1
    basic['other_first_name_2']= e.other_first_name_2
    basic['other_last_name_1']= e.other_last_name_1
    basic['other_last_name_2']= e.other_last_name_2
    basic['other_middle_name_1']= e.other_middle_name_1
    basic['other_middle_name_2']= e.other_middle_name_2
    basic['other_name_code_1']= e.other_name_code_1
    basic['other_name_code_2']= e.other_name_code_2
    basic['other_name_credential_1']= e.other_name_credential_1
    basic['other_name_credential_2']= e.other_name_credential_2
    basic['other_name_prefix_1']= e.other_name_prefix_1
    basic['other_name_prefix_2']= e.other_name_prefix_2
    basic['other_name_suffix_1']= e.other_name_suffix_1
    basic['other_name_suffix_2'] = e.other_name_suffix_2
    


    # Name for organizations
    basic['organization_name']          = e.organization_name
    basic['organization_other_name']    = e.organization_other_name
    basic['organization_other_name_code'] =  e.organization_other_name_code
    basic['organizational_subpart']     = e.organizational_subpart

    
    # PII
    basic['ssn']                = e.ssn
    basic['ein']                = e.ein
    basic['itin']               = e.itin
    basic['gender']             = e.gender
    basic['date_of_birth']      = str(e.date_of_birth)
    basic['state_of_birth']     = e.state_of_birth
    basic['country_of_birth']   = e.country_of_birth
    
    
    # Metadata
    
    #Metadata Dates
    basic['number']                        = e.number
    basic['initial_enumeration_date']       = str(e.initial_enumeration_date)
    basic['enumeration_date']               = str(e.enumeration_date)
    basic['last_updated']                   = str(e.last_updated)
    basic['updated']                        = str(e.updated)
    basic['date_of_death']                  = str(e.date_of_death)
    basic['reactivation_date']              = str(e.reactivation_date) 
     
     
    basic['classification']                 = e.classification
    basic['mode']                           = e.mode
    basic['status']                         = e.status
    basic['contact_method']                 = e.contact_method
    

    basic['deactivated_details']            = e.deactivated_details
    basic['deactivation_date']              = str(e.deactivation_date)
    basic['deactivation_reason_code']       = e.deactivation_reason_code
    basic['decativation_note']              = e.decativation_note
    basic['deceased_notes']                 = e.deceased_notes
    if e.parent_organization:
        basic['parent_organization_npi']    = e.parent_organization.number
    else:
        basic['parent_organization_npi'] = ""
    
    basic['parent_organization_ein']        = e.parent_organization_ein
    basic['parent_organization_legal_business_name'] = e.parent_organization_legal_business_name
    basic['recativation_note']              = e.recativation_note
    basic['comments']                       = e.comments
    
    

    # Authorized Official
    basic['authorized_official_credential']          = e.authorized_official_credential
    basic['authorized_official_email']               = e.authorized_official_email
    basic['authorized_official_first_name']          = e.authorized_official_first_name
    basic['authorized_official_last_name']           = e.authorized_official_last_name
    basic['authorized_official_middle_name']         = e.authorized_official_middle_name
    basic['authorized_official_prefix']              = e.authorized_official_prefix
    basic['authorized_official_suffix']              = e.authorized_official_suffix
    basic['authorized_official_telephone_number']    = e.authorized_official_telephone_number
    basic['authorized_official_telephone_extension'] = e.authorized_official_telephone_extension
    basic['authorized_official_title_or_position']   = e.authorized_official_title_or_position
    
    #Contact Person
    basic['contact_person_credential']          = e.contact_person_credential
    basic['contact_person_email']               = e.contact_person_email
    basic['contact_person_first_name']          = e.contact_person_first_name
    basic['contact_person_last_name']           = e.contact_person_last_name
    basic['contact_person_middle_name']         = e.contact_person_middle_name
    basic['contact_person_prefix']              = e.contact_person_prefix
    basic['contact_person_suffix']              = e.contact_person_suffix
    basic['contact_person_telephone_extension'] = e.contact_person_telephone_extension
    basic['contact_person_telephone_number']    = e.contact_person_telephone_number
    basic['contact_person_title_or_position']   = e.contact_person_title_or_position
    

    #Enhancements/Embilshments
    basic['website']                = e.website
    basic['facebook_handle']        = e.facebook_handle
    basic['twitter_handle']         = e.twitter_handle
    basic['public_email']           = e.public_email
    basic['gravatar_email']         = e.gravatar_email
    basic['driving_directions']     = e.driving_directions       
    basic['bio_headline']           = e.bio_headline

    #Load the basic info into our ordered dictionary
    d['basic'] = basic


    #Addresses
    addresses =[]
    
    #The primary mailing
    if e.mailing_address:
        address = OrderedDict()
        address['address_type']             = e.mailing_address.address_type
        address['address_purpose']          = e.mailing_address.address_purpose
        address['address_1']                = e.mailing_address.address_1
        address['address_2']                = e.mailing_address.address_2
        address['city']                     = e.mailing_address.city
        address['state']                    = e.mailing_address.state
        address['zip']                      = e.mailing_address.zip
        address['country_code']             = e.mailing_address.country_code
        address['foreign_state']            = e.mailing_address.foreign_state
        address['foreign_postal']           = e.mailing_address.foreign_postal
        address['us_telephone_number']      = e.mailing_address.us_telephone_number
        address['us_fax_number']            = e.mailing_address.us_fax_number
        address['foreign_telephone_number'] = e.mailing_address.foreign_telephone_number
        address['foreign_fax_number']       = e.mailing_address.foreign_fax_number
        address['telephone_number_extension']   = e.mailing_address.telephone_number_extension
        addresses.append(address)
    

    #The primary location
    if e.location_address:
        address = OrderedDict()
        address['address_type']             = e.location_address.address_type
        address['address_purpose']          = e.location_address.address_purpose
        address['address_1']                = e.location_address.address_1
        address['address_2']                = e.location_address.address_2
        address['city']                     = e.location_address.city
        address['state']                    = e.location_address.state
        address['zip']                      = e.location_address.zip
        address['country_code']             = e.location_address.country_code
        address['foreign_state']            = e.location_address.foreign_state
        address['foreign_postal']           = e.location_address.foreign_postal
        address['us_telephone_number']      = e.location_address.us_telephone_number
        address['us_fax_number']            = e.location_address.us_fax_number
        address['foreign_telephone_number'] = e.location_address.foreign_telephone_number
        address['foreign_fax_number']       = e.location_address.foreign_fax_number
        address['telephone_number_extension']  = e.location_address.telephone_number_extension
        addresses.append(address)
    
    if e.other_addresses:
        for i in e.other_addresses.all():
            address =OrderedDict()

            address['address_type']             = i.address_type
            address['address_purpose']          = i.address_purpose
            address['address_1']                = i.address_1
            address['address_2']                = i.address_2
            address['city']                     = i.city
            address['state']                    = i.state
            address['zip']                      = i.zip
            address['country_code']             = i.country_code
            address['foreign_state']            = i.foreign_state
            address['foreign_postal']           = i.foreign_postal
            address['us_telephone_number']      = i.us_telephone_number
            address['us_fax_number']            = i.us_fax_number
            address['foreign_telephone_number'] = i.foreign_telephone_number
            address['foreign_fax_number']       = i.foreign_fax_number
            address['telephone_number_extension']  = i.telephone_number_extension
            addresses.append(address)
    
    #Load the addresses into our ordered dictionary
    d['addresses'] = addresses
    

    #build up taxonomies
    taxonomies = []
    if e.taxonomy:
        taxonomy = OrderedDict()
        taxonomy['code'] = e.taxonomy.code
        taxonomy['primary'] = True
        taxonomies.append(taxonomy)
        
        
    
    if e.other_taxonomies:
        
        for i in e.other_taxonomies.all():
            taxonomy = OrderedDict()
            taxonomy['code'] = e.taxonomy.code
            taxonomy['primary'] = False
            taxonomies.append(taxonomy)
            
    d['taxonomies'] = taxonomies
    
    #build up identifiers
    identifiers =[]
    if e.identifiers:
          for i in e.identifiers.all():
            identifier = OrderedDict()
            identifier['identifier'] = i.identifier
            identifier['code']       = i.code
            identifier['state']      =i.state   
            identifier['issuer']     =i.issuer
            identifiers.append(identifier)
    d['identifiers'] = identifiers
    
    #build up identifiers
    specialties =[]
    
    if e.specialty:
        specialty  = OrderedDict()
        specialty['code'] = e.specialty.code
        specialties.append(specialty) 
    
    
    
    if e.specialties:
          for i in e.specialties.all():
            specialty = OrderedDict()
            specialty['code']       = i.code
            specialties.append(specialty)
    d['specialties'] = specialties
    
    
    #build up licenses
    licenses =[]
    
    if e.licenses:
        for i in e.licenses.all():
        
            license  = OrderedDict()
        
            license["number"] = i.number
            license["type"]= i.license_type.license_type
            license["state"]= i.license_type.state
            license["code"]= i.mlvs()
            license["status"]= i.status 
            licenses.append(license) 
    
    d['licenses'] = licenses
    
    
    
    #build up direct addresses
    direct_addresses=[]
    
    if e.direct_addresses:
        for i in e.direct_addresses.all():
        
            da  = OrderedDict()
            da["emailnumber"] = i.email
            da["organization"]= i.organization
            da["public"]= i.public
            direct_addresses.append(da)
    d['direct_addresses'] = direct_addresses

    return json.dumps(d, indent = 4)



def create_basic_html_table(basic):
    
    for k in basic.keys():
        field = e._meta.get_field_by_name(k)
        
        #print dir(field[0])
        is_blank = field[0].blank
        
        if is_blank:
            required = "N"
        else:
            required = "Y"
        
        if field[0].choices:
            l=[]
            for i in field[0].choices:
                l.append(i[0])
            choices = "Choices must be in %s" % (l)
        else:
            choices = ""
        print """ 
    <tr>
      <td>%s</td>
      <td>%s</td>
      <td>%s</td>
      <td>%s</td>
    </tr>
        """ % (k, field[0].max_length, required, choices )
        
def create_address_html_table(address):
    if address:
        field_names = address._meta.get_all_field_names()
        for k in field_names:
            field = address._meta.get_field_by_name(k)
            if field[0].__dict__.has_key("blank"):
                is_blank = field[0].blank
            
            if is_blank:
                required = "N"
            else:
                required = "Y"
            
            
            try:
                if field[0].choices:
                    l=[]
                    for i in field[0].choices:
                        l.append(i[0])
                    choices = "Choices must be in %s" % (l)
                else:
                    choices = ""    
            except:
             choices = ""
            
            
            if field[0].__dict__.has_key("max_length"):
                max_length = field[0].max_length
            else:
                max_length = ""
            
            print """
            <tr>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
            </tr>
                """ % (k, max_length, required, choices )


    