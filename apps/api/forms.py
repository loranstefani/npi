#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
import json, uuid, time
from datetime import datetime, timedelta, date
from pjson.validate import validate_pjson

class ProviderJSONForm(forms.Form):
    
   #The required Fields -------------------------------------------------------    
    provider_json = forms.CharField(max_length=204800,
                           required=False,
                           label="Provider JSON",
                           widget = forms.Textarea())
    required_css_class = 'required'

    
    def clean_provider_json(self):
    
        provider_json = self.cleaned_data.get('provider_json')
        
        try:
            j = json.loads(provider_json)
        except:  
            msg="Provider JSON field does not contain valid JSON."
            raise forms.ValidationError(msg)
        if type(j) != type({}):
            msg="Provider JSON field does not contain a dictionary {}."
            raise forms.ValidationError(msg)
        
        return j


    
    def save(self, update=False, file=None):
        """Custom save for saving to MongoDB"""        
        
        provider_json =  self.cleaned_data.get('provider_json', "")
        print "Save to NPPES RDMS"
        print "Write to read-only DBs"
        