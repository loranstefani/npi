#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
import json, uuid, time
from datetime import datetime, timedelta, date
from pjson.validate import validate_pjson
from utils import sanity_check, change_type_1, change_type_2, new_npi


class ProviderJSONForm(forms.Form):
    
   #The required Fields -------------------------------------------------------    
    provider_json       = forms.CharField(max_length=204800,
                           required=False,
                           label="Provider JSON",
                           widget = forms.Textarea())
    required_css_class  = 'required'

    
    def clean_provider_json(self):
    
        provider_json = self.cleaned_data.get('provider_json')
        
        try:
            j = json.loads(provider_json)
        except:  
            msg="Provider JSON field does not contain valid JSON."
            raise forms.ValidationError(msg)
        
        if type(j) != type({}):
            msg="Provider JSON field does not contain a JSON object {}."
            raise forms.ValidationError(msg)
        
        return provider_json 

    def validate(self):
        provider_json   = self.cleaned_data.get('provider_json')
        errors          = validate_pjson(provider_json)
        if errors:
            return errors
        sanity_check_errors = sanity_check(provider_json)
        if sanity_check_errors:
            return sanity_check_errors
        return []
        

    def get_pjson_object(self):
        provider_json = self.cleaned_data.get('provider_json')
        return json.loads(provider_json)

    
    def save(self, request):
        """Custom save for saving to local DB"""        
        
        provider =  self.get_pjson_object()
        
        if provider['classification'] == "C" and provider['enumeration_type']=="NPI-1":
            print "NPI-1change request"
            errors = change_type_1(provider)
            if not errors:
            
                response = {"message": "NPI-1 change request successful.",
                        "code": 200,
                        "number": provider['number'],
                        "enumeration_type" : provider['enumeration_type']}
            
        elif provider['classification'] == "C" and provider['enumeration_type']=="NPI-2":
            print "NPI-2 change request"
            errors = change_type_2(provider)
            if not errors:
                response = {"message": "NPI-2 change request successful.",
                        "code": 200,
                        "number": provider['number'],
                        "enumeration_type" : provider['enumeration_type']}          
            
            change_type_2, new_type_1, new_type_2    

        
        elif provider['classification'] == "N" and provider['enumeration_type']=="NPI-1":    
            print "NPI-1 new request"
            
            errors = new_npi(provider)
            if not errors:
                response = {"message": "NPI-1 new enumeration request successful.",
                            "code": 200,
                             "number": "123456789",
                             "enumeration_type" : provider['enumeration_type']}
        
        elif provider['classification'] == "N" and provider['enumeration_type']=="NPI-2":    
            print "NPI-2 new request"
            
            errors = new_npi(provider)
            if not errors:
                response = {"message": "NPI-2 new enumeration request successful.",
                            "code":   200,
                            "number": "123456789",
                            "enumeration_type" : provider['enumeration_type']}    
        
        else:
            response = {"message": "No classification was provided so the enumeration request cannot be completed.",
                    "code": 500,
                    "number": "123456789",
                    "enumeration_type" : provider['enumeration_type']}
            
        return response
    
        
        
        