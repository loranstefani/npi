#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
import json, binascii, datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from ..enumerations.models import Enumeration, Event
from ..addresses.models import Address
from ..surrogates.models import Surrogate
from ..licenses.models import License, LicenseType
from ..identifiers.models import Identifier
from ..direct.models import DirectAddress
from ..specialties.models import SpecialtyCode
from ..taxonomy.models import TaxonomyCode
import reversion
from pjson.validate import validate_pjson
from ..enumerations.notifications import (ACTIVATED_BODY, ACTIVATED_SUBJECT)


def validate(body):
        errors = validate_pjson(body)
        if errors:
            return errors
        sanity_check_errors = sanity_check(body)
        if sanity_check_errors:
            return sanity_check_errors
        return []




def save_api_enumeration(request):
        """Custom save for saving to local DB"""        
        
        provider =  json.loads(request.body)
        
        response = {"message": "No classification was provided so the enumeration request cannot be completed.",
                    "code": 500,
                    "status": "ERROR",
                    "enumeration_type" : provider['enumeration_type']}
        
        if provider['classification'] == "C" and provider['enumeration_type'] in ("NPI-1", "NPI-2"):
            #Change request
            enumeration = new_npi(request)
            if enumeration:
                msg = "%s change request successful" % (provider['enumeration_type'])
                response = {"message": msg,
                            "status": "UPDATED",
                            "code": 200,
                            "number": provider['number'],
                            "enumeration_type" : provider['enumeration_type']}
                
        elif provider['classification'] == "N" and provider['enumeration_type'] in ("NPI-1", "NPI-2"):    
            #"New request"
            
            enumeration = new_npi(request)
            if enumeration:
                msg =  "%s new enumeration request successful." % (provider['enumeration_type'])
                response = {"message": msg,
                            "code": 200,
                            "status": "CREATED",
                            "number": enumeration.number,
                            "enumeration_type" : provider['enumeration_type']}
    
        else:
            response = {"message": "No classification was provided so the enumeration request cannot be completed.",
                    "code": 500,
                    "status": "ERROR",
                    "enumeration_type" : provider['enumeration_type']}
            
        return response




def sanity_check(provider_json):
    errors = []
    provider = json.loads(provider_json)
    
    if provider['enumeration_type'] not in ('NPI-1','NPI-2'):
        errors.append("API enumeration is limited to NPI-1 and NPI-2 at this time.")
    
    # If classification=N, then number should not be provided.
    if provider['classification']=="N" and provider.get("number"):
        errors.append("A request for a new enumeration must not contain an enumeration number.")
    
    # If classification=C, then a number should be provided.
    if provider['classification']=="C" and not provider.get("number"):
        errors.append("A change request for an enumeration must contain an enumeration number.")
    
    #If this is a change request, the number should exist.
    if provider['classification']=="C" and not Enumeration.objects.filter(number=provider.get("number")).exists():
        errors.append("The enumeration number provided does not exist.")
    
    if provider['classification']=="N" and provider['enumeration_type']=="NPI-1":
            #check that the DOB is not less than 16 years.
            try:
                date_of_birth = datetime.datetime.strptime(provider['basic'].get('date_of_birth'),
                                                  '%Y-%m-%d').date()
        
                age_days =  datetime.date.today() - date_of_birth
                
                if age_days.days < 5840:
                    errors.append("Candidate must be at least 16 years of age.")
                
            except ValueError:
                errors.append("date_of_birth must be in YYYY-MM-DD format.")
                
            #Make sure the ssn is not already assigned to another npi.
            if provider['basic'].get('ssn'):
                if Enumeration.objects.filter(enumeration_type=provider.get("enumeration_type"),
                                       ssn =  provider['basic'].get('ssn')).exists():
                    errors.append("This ssn already has an existing enumeration number assigned.")
            
            #Make sure the itin is not already assigned to another npi.
            if provider['basic'].get('itin'):
                if Enumeration.objects.filter(enumeration_type=provider.get("enumeration_type"),
                                       ssn =  d['basic'].get('itin')).exists():
                    errors.append("This itin already has an existing enumeration number assigned.")
    
            #Make sure the licenses are not already assigned to someone else.
            for license in provider['licenses']:
                state, license_type, number = license['code'].split("-")
                lt  = LicenseType.objects.get(state = state, license_type=license_type)
                if License.objects.filter(license_type= lt, number=number).exists():
                    error =  "License %s-%s-%s has already been provided by another person."
                    errors.append(error)
    return errors





@reversion.create_revision()
def new_npi(request):
    
    provider =  json.loads(request.body)
    if provider['classification'] == 'N':    
        e = Enumeration()
        change = False
    else:
        e = Enumeration.objects.get(number = provider['number'])
        change = True
    
    e.mode                  = "A" #The mode is API.
    e.website               = provider['basic'].get('website')
    e.facebook_handle       = provider['basic'].get('facebook_handle')
    e.twitter_handle        = provider['basic'].get('twitter_handle')
    e.public_email          = provider['basic'].get('public_email')
    e.gravatar_email        = provider['basic'].get('gravatar_email')
    e.driving_directions    = provider['basic'].get('driving_directions')   
    e.bio_headline          = provider['basic'].get('bio_headline') 
    
    
    if provider['enumeration_type'] == "NPI-1":
        #Basic
        e.enumeration_type = "NPI-1"
        e.name_prefix = provider['basic'].get('name_prefix')
        e.first_name = provider['basic'].get('first_name')
        e.last_name   = provider['basic'].get('last_name')
        e.middle_name = provider['basic'].get('middle_name')
        e.name_suffix = provider['basic'].get('name_suffix')
        e.credential  = provider['basic'].get('credential')  
        e.doing_business_as  = provider['basic'].get('doing_business_as')
        e.sole_proprietor    = provider['basic'].get('sole_proprietor')
        
        e.other_name_prefix_1 = provider['basic'].get('other_name_prefix_1')
        e.other_first_name_1  = provider['basic'].get('other_first_name_1')
        e.other_last_name_1   = provider['basic'].get('other_last_name_1')
        e.other_middle_name_1 = provider['basic'].get('other_middle_name_1')
        e.other_name_suffix_1 = provider['basic'].get('other_name_suffix_1')
        e.other_name_code_1   = provider['basic'].get('other_name_code_1')
        e.other_name_credential_1 = provider['basic'].get('other_name_credential_1')
        
        e.other_name_prefix_2 = provider['basic'].get('other_name_prefix_2')
        e.other_first_name_2  = provider['basic'].get('other_first_name_2')
        e.other_last_name_2   = provider['basic'].get('other_last_name_2')
        e.other_middle_name_2 = provider['basic'].get('other_middle_name_2')
        e.other_name_suffix_2 = provider['basic'].get('other_name_suffix_2')
        e.other_name_code_2   = provider['basic'].get('other_name_code_2')
        e.other_name_credential_2       = provider['basic'].get('other_name_credential_2')
        
        e.contact_person_credential     = provider['basic'].get('contact_person_credential')
        e.contact_person_email          = provider['basic'].get('contact_person_email')
        e.contact_person_first_name     = provider['basic'].get('contact_person_first_name')
        e.contact_person_last_name      = provider['basic'].get('contact_person_last_name')
        e.contact_person_middle_name    = provider['basic'].get('contact_person_middle_name')
        e.contact_person_prefix         = provider['basic'].get('contact_person_prefix')
        e.contact_person_suffix         = provider['basic'].get('contact_person_suffix')
        e.contact_person_telephone_extension    = provider['basic'].get('contact_person_telephone_extension')
        e.contact_person_telephone_number       = provider['basic'].get('contact_person_telephone_number')
        e.contact_person_title_or_position      = provider['basic'].get('contact_person_title_or_position')
        e.date_of_birth                         =  datetime.datetime.strptime(provider['basic'].get('date_of_birth'), '%Y-%m-%d').date()   
        e.ssn = provider['basic'].get('ssn')
        e.itin= provider['basic'].get('itin')
        e.gender= provider['basic'].get('gender')
        e.state_of_birth= provider['basic'].get('state_of_birth')
        e.country_of_birth= provider['basic'].get('country_of_birth')
    
    if provider['enumeration_type'] == "NPI-2":
        e.enumeration_type = "NPI-2"
        e.ein = provider['basic'].get('ein')
        # Name for organizations
        e.organization_name              = provider['basic'].get('organization_name ')
        e.organization_other_name        = provider['basic'].get('organization_other_name')
        e.organization_other_name_code   = provider['basic'].get('organization_other_name_code')
        e.organizational_subpart         = provider['basic'].get('organizational_subpart')
        e.authorized_official_credential = provider['basic'].get('authorized_official_credential')

        e.authorized_official_prefix        = provider['basic'].get('authorized_official_prefix=')
        e.authorized_official_credential    = provider['basic'].get('uthorized_official_credential')
        e.authorized_official_email         = provider['basic'].get('authorized_official_email')
        e.authorized_official_first_name    = provider['basic'].get('authorized_official_first_name')
        e.authorized_official_last_name     = provider['basic'].get('uthorized_official_last_name')
        e.authorized_official_middle_name   = provider['basic'].get('authorized_official_middle_name')
    
        e.authorized_official_suffix                = provider['basic'].get('authorized_official_suffix')
        e.authorized_official_telephone_number      = provider['basic'].get('authorized_official_telephone_number')
        e.authorized_official_telephone_extension   = provider['basic'].get('authorized_official_telephone_extension')
        e.authorized_official_title_or_position     = provider['basic'].get('authorized_official_title_or_position')
    
    e.save()
    if change:
        if e.mailing_address:
            e.mailing_address.delete()
        if e.mailing_address:
            e.mailing_address.delete()
        
        for a in e.other_addresses.all():
            if a:
                a.delete()
        
    for address in provider['addresses']:
        
        
        
        if address['address_purpose'] == "MAILING":
            a = Address(address_type      =  address['address_type'],
                    address_purpose   =  address['address_purpose'],
                    address_1         =  address['address_1'],
                    address_2         =  address.get('address_2'),
                    city              =  address.get('city'),
                    state             =  address.get('state'),
                    zip               =  address.get('zip'),
                    mpo               =  address.get('mpo',""),
                    country_code      =  address.get('country_code'),
                    foreign_state     =  address.get('foreign_state'),
                    foreign_postal    =  address.get('foreign_postal'),
                    us_telephone_number        =  address.get('us_telephone_number'),
                    us_fax_number              =  address.get('us_fax_number'),
                    foreign_telephone_number   =  address.get('foreign_telephone_number'),
                    foreign_fax_number         =  address.get('foreign_fax_number'),
                    telephone_number_extension =  address.get('telephone_number_extension'),
                    )
            a.save()
            e.mailing_address = a
            
        elif address['address_purpose'] == "LOCATION":
            a = Address(address_type      =  address['address_type'],
                    address_purpose   =  address['address_purpose'],
                    address_1         =  address['address_1'],
                    address_2         =  address.get('address_2'),
                    city              =  address.get('city'),
                    state             =  address.get('state'),
                    zip               =  address.get('zip'),
                    mpo               =  address.get('mpo',""),
                    country_code      =  address.get('country_code'),
                    foreign_state     =  address.get('foreign_state'),
                    foreign_postal    =  address.get('foreign_postal'),
                    us_telephone_number        =  address.get('us_telephone_number'),
                    us_fax_number              =  address.get('us_fax_number'),
                    foreign_telephone_number   =  address.get('foreign_telephone_number'),
                    foreign_fax_number         =  address.get('foreign_fax_number'),
                    telephone_number_extension =  address.get('telephone_number_extension'),
                    )
            a.save()
            e.location_address = a
        
        else:
            a = Address(address_type      =  address['address_type'],
                    address_purpose   =  address['address_purpose'],
                    address_1         =  address['address_1'],
                    address_2         =  address.get('address_2'),
                    city              =  address.get('city'),
                    state             =  address.get('state'),
                    zip               =  address.get('zip'),
                    mpo               =  address.get('mpo',""),
                    country_code      =  address.get('country_code'),
                    foreign_state     =  address.get('foreign_state'),
                    foreign_postal    =  address.get('foreign_postal'),
                    us_telephone_number        =  address.get('us_telephone_number'),
                    us_fax_number              =  address.get('us_fax_number'),
                    foreign_telephone_number   =  address.get('foreign_telephone_number'),
                    foreign_fax_number         =  address.get('foreign_fax_number'),
                    telephone_number_extension =  address.get('telephone_number_extension'),
                    )
            a.save()
            e.other_addresses.add(a)   
    
    #Licenses
    if change:
        for license in e.licenses.all():
            license.delete()
    
    for license in provider['licenses']:
        state, license_type, number = license['code'].split("-")
        lt  = LicenseType.objects.get(state = state, license_type=license_type)
        l = License(license_type= lt, number=number)
        l.save()
        e.licenses.add(l)
    
    #Identifiers
    if change:
        for identifier in e.identifiers.all():
            identifier.delete()
    
    for identifier in provider['identifiers']:
        
        i = Identifier(identifier = identifier['identifier'],
                       code =identifier['code'],
                       state =identifier['state'],
                       issuer = identifier['issuer'])
        i.save()
        e.identifiers.add(i)
              
    
    #Taxonomies
    if change:
        if e.taxonomy:
            e.taxonomy.delete()
        
        for taxonomy in e.other_taxonomies.all():
            taxonomy.delete()
    
    for taxonomy in provider['taxonomies']:
        if taxonomy['primary'] == True:
            tc = TaxonomyCode.objects.get(code= taxonomy['code'])
            e.taxonomy = tc
        elif taxonomy['primary'] == False:
            tc = TaxonomyCode.objects.get(code= taxonomy['code'])
            e.other_taxonomies.add(tc)
            
    #Direct Addresses
    if change:
        for direct_address in e.direct_addresses.all():
            direct_address.delete()
    
    for direct_address in provider['direct_addresses']:
        d = DirectAddress(email = direct_address['email'],
                          organization=direct_address['organization'],
                          public  =direct_address['public'])
        d.save()
        e.direct_addresses.add(d)
    
    
    #Save and activate the NPI
    e.status          = "A"
    e.enueration_date = datetime.date.today()
    e.last_update     = datetime.date.today()
    e.last_updated_ip = request.META['REMOTE_ADDR']
    system_user       = User.objects.get(username=settings.AUTO_ENUMERATION_USERNAME)
    e.enumerated_by   = system_user
    e.managers.add(request.user)
    s = Surrogate.objects.get(user=request.user)
    s.save()
    s.enumerations.add(e)
    s.save()
    
    e.save()
    if change:
        msg = "The application has been automaticaly updated via the API. The number issued is %s." % (e.number)
        Event.objects.create(enumeration=e, event_type="ACTIVATION",
                          body = ACTIVATED_BODY, 
                          subject = ACTIVATED_SUBJECT, 
                          note= msg)
    
    else:
        msg = "The application has been automaticaly enumerated via the API. The number issued is %s." % (e.number)
        #Create an Event
        Event.objects.create(enumeration=e, event_type="ACTIVATION",
                          body = ACTIVATED_BODY, 
                          subject = ACTIVATED_SUBJECT, 
                          note= msg)
    
    #Create a revision for the model
    reversion.set_comment("Submit Enumeration Application - Auto-Enumerated via API")
    reversion.set_user(request.user)
    return e











def get_unauthenticated_response(request):
    auth_string = request.META.get('HTTP_AUTHORIZATION', None)
    
    
    #if none then the user was authenticated.
    response = None 
    
    if not auth_string:
        jsonstr={"code": 401,
                 "status": "ERROR",
                 "message": "No HTTP_AUTHORIZATION supplied.",
                 "errors": ["No HTTP_AUTHORIZATION supplied.", ]
                 }
        jsonstr=json.dumps(jsonstr, indent = 4,)
        response = HttpResponse(jsonstr) 
    else:
    
    
        
        try:
            (authmeth, auth) = auth_string.split(" ", 1)
    
            if not authmeth.lower() == 'basic':
                jsonstr={"code": 401,
                          "status": "ERROR",
                          "message": "No HTTP_AUTHORIZATION supplied.",
                          "errors": ["No HTTP_AUTHORIZATION supplied.", ]
                          }
                jsonstr=json.dumps(jsonstr, indent = 4,)
                response = HttpResponse(jsonstr, mimetype="application/json")
    
            
            #information was supplied
            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)
            #authenticate
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    #the account is disabled
                    jsonstr={"code": 401,  "status": "ERROR",
                             "message": "Account disabled.",
                             "errors": ["Account disabled.", ]
                             }
                    jsonstr=json.dumps(jsonstr, indent = 4,)
                    response =  HttpResponse(jsonstr, mimetype="application/json")
                else:
                    #login the user
                    login(request, user)
            else:
                # the authentication system was unable to verify the username and password
                jsonstr={"code": 401,  "status": "ERROR",
                         "message": "Invalid username or password.",
                         "errors": ["Invalid username or password." ,]}
                jsonstr=json.dumps(jsonstr, indent = 4,)
                response =  HttpResponse(jsonstr, mimetype="application/json")
            
        
        except (ValueError, binascii.Error):
            jsonstr={"code": 401,  "status": "ERROR",
                     "message": "No HTTP_AUTHORIZATION supplied.",
                     "errors": ["No HTTP_AUTHORIZATION supplied.", ]
                     }
            jsonstr=json.dumps(jsonstr, indent = 4,)
            response =  HttpResponse(jsonstr, mimetype="application/json")
    
    return response
    
     
       
    