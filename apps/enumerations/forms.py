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



class SelectAddressTypeForm(ModelForm):
    class Meta:
        model = Address
        fields = ('address_type',)
    required_css_class = 'required'
    
    
class DomesticAddressForm(ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(DomesticAddressForm,self).__init__(*args,**kwargs)
        self.fields['state'].choices=US_STATES
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'state', 'zip')
    
    country_code = forms.CharField(widget= forms.HiddenInput, initial="US")
    required_css_class = 'required'
    
    
class ForeignAddressForm(ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(ForeignAddressForm,self).__init__(*args,**kwargs)
        
    
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'foreign_state',
                  'foreign_postal', 'country_code')
        
    state = forms.CharField(widget= forms.HiddenInput, initial="ZZ")
        
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
    
    country_code = forms.CharField(widget= forms.HiddenInput, initial="US")