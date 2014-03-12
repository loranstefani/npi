#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from models import License, LicenseValidator
import datetime
from localflavor.us.us_states import US_STATES
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from utils import (build_mlvs_url, compare_license_number_to_mlvsjson,
                   query_mlvs_server)

class AutoVerifyLicenseForm(ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""    
        super(AutoVerifyLicenseForm,self).__init__(*args,**kwargs)
        self.fields['number'].required = True
        self.fields['license_type'].required = True
       
    class Meta:
        model = License
        fields = ('license_type', 'number',)
    
    required_css_class = 'required'


    def clean_license_type(self):
        license_type  = self.cleaned_data.get('license_type')

        state = license_type
            
        try:
            lv = LicenseValidator.objects.get(license_type=license_type)
            
        except LicenseValidator.DoesNotExist:
            raise forms.ValidationError("This issuing body does not support automatic license verification. You can still enter it manually.")
        
        return license_type



    def clean(self):
        cleaned_data = super(AutoVerifyLicenseForm, self).clean()
        number = cleaned_data.get('number')
        license_type  = cleaned_data.get('license_type')
        
        if number and license_type:
            try:
                lv = LicenseValidator.objects.get(license_type=license_type)
            except LicenseValidator.DoesNotExist:
                msg = """This issuing body does not support automatic license verification. You can still enter it manually."""
                raise forms.ValidationError(msg)
      
            url = build_mlvs_url(lv.url,  number)
            
            print url
            mvls = query_mlvs_server(url)
            
            if not query_mlvs_server(url):
                raise forms.ValidationError("The license issuing body appears to be participating in automatic license verification, but this license was not found.")
            
            if not compare_license_number_to_mlvsjson(license_type.state, number, license_type.license_type, mvls):
                msg = "The license was found but details did not align. See %s for more details." % (url)
                raise forms.ValidationError(msg)
        return cleaned_data
    
    
    
    

class CreateLicenseForm(ModelForm):
    
    class Meta:
        model = License
        fields = ('license_type', 'number', 'license_image', 'note',)
    

    required_css_class = 'required'

        


