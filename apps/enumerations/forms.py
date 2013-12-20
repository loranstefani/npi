#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from models import Address, Enumeration, License
import datetime

from django.utils.translation import ugettext_lazy as _



class SelectAddressTypeForm(ModelForm):
    class Meta:
        model = Address
        fields = ('address_type',)
    required_css_class = 'required'
    
    
    
class DomesticAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('address_1', 'address_2', 'city', 'state', 'zip')
    required_css_class = 'required'