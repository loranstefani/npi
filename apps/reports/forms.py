#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django import forms
from ..enumerations.models import (ENUMERATION_TYPE_CHOICES, Enumeration,
                                   ENUMERATION_MODE_CHOICES,
                                   ENUMERATION_CLASSIFICATION_CHOICES )
from django.db.models import Count
from django.contrib.auth.models import User
def report_year_range():
    this_year = datetime.date.today().year
    years = range(2005, this_year+1)
    return years


ENUMERATION_TYPE_WITH_ALL_CHOICES = [(None, "All"), ] +  list(ENUMERATION_TYPE_CHOICES)

def default_from_date(subtract_days=60):
    return datetime.date.today() - datetime.timedelta(days=subtract_days)
    
    this_year = datetime.date.today().year




class PendingEnumerationForm(forms.Form):
    
    enumeration_type    = forms.ChoiceField(choices = ENUMERATION_TYPE_CHOICES)
    required_css_class  = 'required'
    
    def save(self):
         enumeration_type = self.cleaned_data.get("enumeration_type")
         qs = Enumeration.objects.filter(status = "P")
         return qs
        
        

class PendingEnumerationOverviewForm(forms.Form):
    
    date_since  = forms.DateField( widget    = SelectDateWidget(
                                    years   = report_year_range()),
                                    initial = default_from_date)
                                    
    #date_since   = forms.DateField(initial=datetime.date.today,           
    #                        widget=SelectDateWidget( years=report_year_range()))
    
    enumeration_type    = forms.ChoiceField(choices = ENUMERATION_TYPE_WITH_ALL_CHOICES)
    classification  = forms.ChoiceField(choices =ENUMERATION_CLASSIFICATION_CHOICES)
    mode            = forms.ChoiceField(choices = ENUMERATION_MODE_CHOICES)
        
    required_css_class  = 'required'
    
    def save(self):
          
         
        enumeration_type = self.cleaned_data.get("enumeration_type")
        date_since = self.cleaned_data.get("date_since")
        classification = self.cleaned_data.get("classification")
        mode = self.cleaned_data.get("mode")

        
        
        if enumeration_type:
            qs = Enumeration.objects.filter(enumeration_type = enumeration_type,
                                            mode = mode,
                                            classification = classification) \
                .exclude(last_updated__gte=datetime.date.today) \
                .exclude(last_updated__lt=date_since)
        else:
             qs = Enumeration.objects.filter(mode = mode,
                                            classification = classification)\
                .exclude(last_updated__gte=datetime.date.today) \
                .exclude(last_updated__lt=date_since) 
        

        total                     = qs.filter()
        total_field               = total.filter(field_error=True)
        total_license             = total.filter(license_error=True)
        total_license_taxonomy    = total.filter(license_taxonomy_error=True)
        total_location_address    = total.filter(location_address_error=True )
        total_mailing_address     = total.filter(mailing_address_error=True)
        total_invalid_ssn         = total.filter(invalid_ssn_error=True)
        total_invalid_ein         = total.filter(invalid_ein_error=True)
        total_ssn_already_issued  = total.filter(ssn_already_issued_error=True)            

        
        
        # one to five 
        # create a date 5 days from today
        fda = datetime.date.today() - datetime.timedelta(days=5)
        one_to_five = qs.filter(last_updated__gte=fda)
        one_to_five_field  = one_to_five .filter()
        one_to_five_license = one_to_five .filter()
        one_to_five_license_taxonomy = one_to_five .filter()
        one_to_five_location_address = one_to_five .filter()
        one_to_five_mailing_address = one_to_five .filter()
        one_to_five_ssn = qs.filter()
        one_to_five_ein = qs.filter()
        
        
        results = {"one_to_five": one_to_five}
        return results



   
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
        
        if not staff_user:
            """Display Everything"""    
            activations = Enumeration.objects.filter(status="A").exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).values('enumerated_by__username').annotate(Count('id'))
            total_activations = Enumeration.objects.filter(status="A").exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
            total_enumerations = Enumeration.objects.filter().exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
            total_rejections = Enumeration.objects.filter(status="R").exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
        else:
            activations = Enumeration.objects.filter(status="A", enumerated_by=staff_user).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).values('enumerated_by__username').annotate(Count('id'))
            total_activations = Enumeration.objects.filter(status="A", enumerated_by=staff_user).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
            total_enumerations = Enumeration.objects.filter(enumerated_by=staff_user).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
            total_rejections = Enumeration.objects.filter(status="R", enumerated_by=staff_user).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
        
        return {'activations': activations,
                'total_activations':total_activations,
                'total_enumerations':total_enumerations,
                'total_rejections': total_rejections}        
        
        
        
        
         
    