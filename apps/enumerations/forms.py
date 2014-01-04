#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from models import Address, Enumeration, License
import datetime
from localflavor.us.us_states import US_STATES
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from countries import NO_US_COUNTRIES, US_COUNTRY_CHOICES



class SearchForm(ModelForm):
    class Meta:
        model = Enumeration
        fields = (
                  'number', 'first_name', 'last_name', 'organization_name',
                  )
    required_css_class = 'required'
    
    def save(self, force_insert=False, force_update=False, commit=True):
        
        q={}
        number              = self.cleaned_data.get("number", "")
        first_name          = self.cleaned_data.get("first_name", "")
        last_name           = self.cleaned_data.get("last_name", "")
        organization_name   = self.cleaned_data.get("organization_name", "")
        
        
        if number:
            q['number']=number
        
        if first_name:
            q['first_name']=first_name
        
        if last_name:
            q['last_name']=last_name
        
        if organization_name:
            q['organization_name']=organization_name
        
            
        qs = Enumeration.objects.filter(**q)
        for i in qs:
            print i
        return qs
    
    


class CreateEnumeration1Form(ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        
        mymanager = kwargs.pop('mymanager', None)        
        super(CreateEnumeration1Form,self).__init__(*args,**kwargs)
        
        if mymanager:
            #self.fields['managers'].widget  = forms.CheckboxSelectMultiple
            self.fields['managers'].queryset = User.objects.filter(email=mymanager)
            self.fields['managers'].initial  = User.objects.filter(email=mymanager)
            self.fields['managers'].required = True
            self.fields['enumeration_type'].required = True
            
    class Meta:
        model = Enumeration
        fields = ('enumeration_type', 'managers')
    manager = forms.CharField(widget= forms.HiddenInput, required=False,
                                   initial="")
    required_css_class = 'required'

class CreateEnumerationOrganizationForm(ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(CreateEnumerationOrganizationForm,self).__init__(*args,**kwargs)
        self.fields['organization_name'].required = True
        self.fields['tein'].required = True
        self.fields['tein'].help_text = "EINs are issued by the IRS. This is required for organizations."
        self.fields['contact_person_email'].required = True
        self.fields['contact_person_first_name'].required = True
        self.fields['contact_person_last_name'].required = True
        self.fields['primary_taxonomy'].required = True

        
    class Meta:
        model = Enumeration
        fields = ('organization_name', 'tein', 'doing_business_as',
                  'phone_number', 'fax_number',
                  'contact_person_email', 'contact_person_first_name',
                   'contact_person_last_name', 'contact_person_telephone' ,
                    'contact_person_extension', 'primary_taxonomy'
                  )
    required_css_class = 'required'
    


class CreateEnumerationIndividualForm(ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(CreateEnumerationIndividualForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['tein'].help_text = "EINs are issued by the IRS. This is optional for individuals."
        self.fields['contact_person_email'].required = True
        self.fields['contact_person_first_name'].required = True
        self.fields['contact_person_last_name'].required = True
        self.fields['primary_taxonomy'].required = True      
    class Meta:
        model = Enumeration
        fields = ('first_name', 'last_name', 'ssn', 'sole_protieter',
                  'doing_business_as', 'tein',
                  'phone_number', 'fax_number',
                  'other_first_name_1',                  
                    'other_last_name_1', 'other_first_name_2', 'other_last_name_2',
                    'contact_person_email', 'contact_person_first_name',
                    'contact_person_last_name', 'contact_person_telephone' ,
                    'contact_person_extension', 'primary_taxonomy')
        
    required_css_class = 'required'


class EnumerationEnhancementForm(ModelForm):
    class Meta:
        model = Enumeration
        fields = (
                  'website', 'driving_directions',
                  'hours_of_operation', 'bio',
                  'avatar_image', 'background_image',
                  )
    required_css_class = 'required'



class AddParentForm(forms.Form):
    
    
    number = forms.CharField(max_length=20, initial="", label="Number (e.g. NPI, OEID)")
    required_css_class = 'required'


class SelectAddressTypeForm(ModelForm):
    class Meta:
        model = Address
        fields = ('address_type', 'address_purpose')
    required_css_class = 'required'
    




class SelectAddressPurposeForm(ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        
        address_purpose = str(kwargs.pop('address_purpose', None)) 
        
        super(SelectAddressPurposeForm,self).__init__(*args,**kwargs)
        if address_purpose:
            self.fields['address_purpose'].initial = address_purpose

            if address_purpose == "PRIMARY-LOCATION":
                self.fields['address_purpose'].choices = ((address_purpose,'Primary Practice/Business Address (Phyiscal)'),)
            
            if address_purpose == "PRIMARY-BUSINESS":
                self.fields['address_purpose'].choices = ((address_purpose,'Primary Business Correspondence Address'),)
 
            if address_purpose == "MEDREC-STORAGE":
                self.fields['address_purpose'].choices = ((address_purpose,'Medical Records Storage Address'),)

            if address_purpose == "1099":
                self.fields['address_purpose'].choices = ((address_purpose,'1099 Address'),) 

            if address_purpose == "REVALIDATION":
                self.fields['address_purpose'].choices = ((address_purpose,'Revalidation Address'),) 

            if address_purpose == "ADDITIONAL-PRACTICE":
                self.fields['address_purpose'].choices = ((address_purpose,'Additional Practice Address'),) 

            if address_purpose == "ADDITIONAL-BUSINESS":
                self.fields['address_purpose'].choices = ((address_purpose,'Additional Business Address'),) 

            if address_purpose == "OTHER":
                self.fields['address_purpose'].choices = (
                        ("ADDITIONAL-PRACTICE",  "Additional Practice Address"),
                        ("ADDITIONAL-BUSINESS",  "Additional Business Address"),
                        )


    class Meta:
        model = Address
        fields = ('address_type', 'address_purpose')
    required_css_class = 'required'


class DomesticAddressForm(ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(DomesticAddressForm,self).__init__(*args,**kwargs)
        self.fields['state'].choices=US_STATES
        self.fields['country_code'].choices=US_COUNTRY_CHOICES
        self.fields['country_code'].initial="US"
        self.fields['country_code'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['zip'].required = True
        
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'state', 'zip', 'country_code',
                  'us_phone_number','us_fax_number')
    
    address_type = forms.CharField(widget= forms.HiddenInput, initial="DOM")

    required_css_class = 'required'
    


    
class ForeignAddressForm(ModelForm):

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
                  'foreign_postal', 'country_code', 'foreign_phone_number',
                  'foreign_fax_number')
        
    state = forms.CharField(widget= forms.HiddenInput, initial="ZZ")
    address_type = forms.CharField(widget= forms.HiddenInput, initial="FGN")

        
    required_css_class = 'required'
    
    
class MilitaryAddressForm(ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(MilitaryAddressForm,self).__init__(*args,**kwargs)
        MIL_CHOICES = (('AE', 'AE - (ZIPs 09xxx) Armed Forces Europe which includes Canada, Middle East, and Africa'),
                       ('AP', 'AP - (ZIPs 962xx) Armed Forces Pacific'),
                       ('AA', 'AA - (ZIPs 340xx) Armed Forces (Central and South) Americas'))
                      
        self.fields['state'].choices=MIL_CHOICES
        self.fields['mpo'].required = True
        self.fields['zip'].required = True
        
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'mpo', 'state', 'zip',
                  'us_phone_number', 'us_fax_number')
    
    required_css_class = 'required'
    
    country_code    = forms.CharField(widget= forms.HiddenInput, initial="US")