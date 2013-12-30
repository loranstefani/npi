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
    
    class Meta:
        model = Enumeration
        fields = ('organization_name', 'tein', 'doing_business_as',
                  )
    required_css_class = 'required'
    


class CreateEnumerationIndividualForm(ModelForm):
    class Meta:
        model = Enumeration
        fields = ('first_name', 'last_name', 'ssn', 'sole_protieter',
                  'doing_business_as', 'tein',
                  )
    required_css_class = 'required'


class AdditionalInformationForm(ModelForm):
    class Meta:
        model = Enumeration
        fields = ('primary_business_address','primary_practice_address', 'licenses',
                  'website', 'driving_directions', 'hours_of_operation', 'bio',
                  'avatar_image', 'background_image',
                  )
    required_css_class = 'required'





class SelectAddressTypeForm(ModelForm):
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
        
        

    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'state', 'zip', 'country_code')
    
    country_code = forms.TypedChoiceField(initial="US", choices=US_COUNTRY_CHOICES)
    address_type = forms.CharField(widget= forms.HiddenInput, initial="DOM")

    
    required_css_class = 'required'
    
    
class ForeignAddressForm(ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(ForeignAddressForm,self).__init__(*args,**kwargs)
        self.fields['country_code'].choices=NO_US_COUNTRIES
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'foreign_state',
                  'foreign_postal', 'country_code')
        
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
        
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'mpo', 'state', 'zip',)
    required_css_class = 'required'
    
    country_code    = forms.CharField(widget= forms.HiddenInput, initial="US")