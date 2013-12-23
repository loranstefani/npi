#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from localflavor.us.us_states import US_STATES
from django.utils.translation import ugettext_lazy as _



class SearchForm(forms.Form):
    
    
    npi = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    state  = forms.CharField(required=False)
    taxonomy = forms.CharField(required=False)
    required_css_class = 'required'