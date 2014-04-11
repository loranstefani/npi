#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django import forms
from ..enumerations.models import ENUMERATION_TYPE_CHOICES, Enumeration


def report_year_range():
    this_year = datetime.date.today().year
    years = range(2005, this_year)
    return years


class PendingEnumerationForm(forms.Form):
    
    enumeration_type    = forms.ChoiceField(choices = ENUMERATION_TYPE_CHOICES)
    
    
    required_css_class  = 'required'
    
    def save(self, force_insert=False, force_update=False, commit=True):
         
         #date_start = self.cleaned_data.get("date_start")
         #date_stop =  self.cleaned_data.get("date_stop")
         enumeration_type = self.cleaned_data.get("enumeration_type")
         qs = Enumeration.objects.filter(status = "P")

         return qs
        
class DateRangeForm(forms.Form):
    date_start  = forms.DateField(widget=SelectDateWidget(
                                    years=report_year_range()),
                                    initial=datetime.date(2005,05,23))
                                    
    date_stop   = forms.DateField(initial=datetime.date.today,           
                            widget=SelectDateWidget( years=report_year_range()))
                                                            
                                    
    

    
    
    required_css_class  = 'required'
    
    def save(self, force_insert=False, force_update=False, commit=True):
         
         date_start = self.cleaned_data.get("date_start")
         date_stop =  self.cleaned_data.get("date_stop")
         enumeration_type = self.cleaned_data.get("enumeration_type")
         qs = Enumeration.objects.filter(status = "P")

         return qs