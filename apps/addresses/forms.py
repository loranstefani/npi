#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from models import Address, US_STATE_CHOICES, MILITARY_STATE_CHOICES
import datetime
from django.utils.translation import ugettext_lazy as _
from countries import NO_US_COUNTRIES, US_COUNTRY_CHOICES


class SelectAddressTypeForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address_type', 'address_purpose')
    required_css_class = 'required'
    

class SelectAddressPurposeForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        
        address_purpose = str(kwargs.pop('address_purpose', None)) 
        
        super(SelectAddressPurposeForm,self).__init__(*args,**kwargs)
        if address_purpose:
            self.fields['address_purpose'].initial = address_purpose

            if address_purpose == "LOCATION":
                self.fields['address_purpose'].choices = ((address_purpose,'Location Address (Phyiscal)'),)
            
            if address_purpose == "MAILING":
                self.fields['address_purpose'].choices = ((address_purpose,'Mailing Address (Correspondence)'),)
 
            if address_purpose == "MEDREC-STORAGE":
                self.fields['address_purpose'].choices = ((address_purpose,'Medical Records Storage Address'),)

            if address_purpose == "1099":
                self.fields['address_purpose'].choices = ((address_purpose,'1099 Address'),) 

            if address_purpose == "REVALIDATION":
                self.fields['address_purpose'].choices = ((address_purpose,'Revalidation Address'),) 

            if address_purpose == "ADDITIONAL-LOCATION":
                self.fields['address_purpose'].choices = ((address_purpose,'Additional Location Address (Physical)'),) 

            if address_purpose == "OTHER":
                self.fields['address_purpose'].choices = (
                        ("ADDITIONAL-LOCATION",  "Additional Practice Address"),
                        )


    class Meta:
        model = Address
        fields = ('address_type', 'address_purpose' )
    required_css_class = 'required'


class DomesticAddressForm(forms.ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(DomesticAddressForm,self).__init__(*args,**kwargs)
        self.fields['state'].choices=US_STATE_CHOICES
        self.fields['country_code'].choices=US_COUNTRY_CHOICES
        self.fields['country_code'].initial="US"
        self.fields['country_code'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['zip'].required = True
        
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'state', 'zip', 'country_code',
                  'us_telephone_number','us_fax_number')
    
    address_type = forms.CharField(widget= forms.HiddenInput, initial="DOM")

    required_css_class = 'required'



class DomesticAddress2Form(forms.ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(DomesticAddress2Form,self).__init__(*args,**kwargs)
        #self.fields['state'].choices=US_STATE_CHOICES
        #self.fields['country_code'].choices=US_COUNTRY_CHOICES
        self.fields['country_code'].initial="US"
        self.fields['country_code'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['zip'].required = True
        
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'state', 'zip', 'country_code',
                  'us_telephone_number','us_fax_number')
    
    
    address_type = forms.CharField(widget= forms.HiddenInput, initial="DOM")
    state        = forms.CharField()
    country_code      = forms.CharField()


    required_css_class = 'required'

  


    
class ForeignAddressForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(ForeignAddressForm,self).__init__(*args,**kwargs)
        self.fields['country_code'].choices=NO_US_COUNTRIES
        self.fields['country_code'].required = True
        self.fields['city'].required = True
        self.fields['foreign_postal'].required = True
        self.fields['country_code'].required = True
    
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'foreign_state',
                  'foreign_postal', 'country_code', 'foreign_telephone_number',
                  'foreign_fax_number')
        
    state = forms.CharField(widget= forms.HiddenInput, initial="ZZ")
    address_type = forms.CharField(widget= forms.HiddenInput, initial="FGN")

        
    required_css_class = 'required'
    
    
class MilitaryAddressForm(forms.ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(MilitaryAddressForm,self).__init__(*args,**kwargs)                      
        self.fields['state'].choices=MILITARY_STATE_CHOICES
        self.fields['mpo'].required = True
        self.fields['zip'].required = True
        
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'mpo', 'state', 'zip',
                  'us_telephone_number', 'us_fax_number')
    
    required_css_class = 'required'
    
    country_code    = forms.CharField(widget= forms.HiddenInput, initial="US")