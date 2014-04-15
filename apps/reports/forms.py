#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django import forms
from ..enumerations.models import ENUMERATION_TYPE_CHOICES, Enumeration
from django.db.models import Count
from django.contrib.auth.models import User
def report_year_range():
    this_year = datetime.date.today().year
    years = range(2005, this_year+1)
    return years


class PendingEnumerationForm(forms.Form):
    
    enumeration_type    = forms.ChoiceField(choices = ENUMERATION_TYPE_CHOICES)
    required_css_class  = 'required'
    
    def save(self):
         enumeration_type = self.cleaned_data.get("enumeration_type")
         qs = Enumeration.objects.filter(status = "P")
         return qs
        
        
        
class EnumerationsStatisByStateForm(forms.Form):
    date_start  = forms.DateField(widget=SelectDateWidget(
                                    years=report_year_range()),
                                    initial=datetime.date(2005,05,23))
                                    
    date_stop   = forms.DateField(initial=datetime.date.today,           
                            widget=SelectDateWidget( years=report_year_range()))
                                                            
    required_css_class  = 'required'
    
    def save(self):
            
        date_start = self.cleaned_data.get("date_start")
        date_stop =  self.cleaned_data.get("date_stop")
         
        #By state and type
        qs = Enumeration.objects.exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).values('location_address__state', 'mode').annotate(Count('id'))
         
        #Totals per state
        state_totals = Enumeration.objects.values('location_address__state').annotate(Count('id'))
         
        #Totals per mode
        mode_totals = Enumeration.objects.values('mode').annotate(Count('id'))
        
        #Total
        total_enumerations = Enumeration.objects.all().count()
         
         
        return { 'state_and_type':      qs,
                 'state_totals':        state_totals,
                 'mode_totals':         mode_totals,
                 'total_enumerations':  total_enumerations
                 }
        
class EnumeratedApplicationsForm(forms.Form):
    
    date_start  = forms.DateField(widget=SelectDateWidget(
                                    years=report_year_range()),
                                    initial=datetime.date(2005,05,23))
                                    
    date_stop   = forms.DateField(initial=datetime.date.today,           
                            widget=SelectDateWidget( years=report_year_range()))
    
    staff_user = forms.ModelChoiceField(queryset = User.objects.filter(is_staff=True), required=False)
                                                            
    required_css_class  = 'required'
    
    def save(self):
            
        date_start = self.cleaned_data.get("date_start")
        date_stop =  self.cleaned_data.get("date_stop")
        staff_user = self.cleaned_data.get("staff_user", None)
        
        print staff_user, type(staff_user)
        
        if not staff_user:
            """Display Everything"""    
            qs = Enumeration.objects.filter(status="A").exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).values('enumerated_by__username').annotate(Count('id'))
        
        else:
            qs = Enumeration.objects.filter(status="A", enumerated_by=staff_user).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).values('enumerated_by__username').annotate(Count('id'))
        
        
        return qs        
        
        
        
        
         
    