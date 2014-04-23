#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django import forms
from ..enumerations.models import (Enumeration, GateKeeperError,
                                   ENUMERATION_TYPE_CHOICES, 
                                   ENUMERATION_MODE_CHOICES,
                                   ENUMERATION_CLASSIFICATION_CHOICES,
                                   ENUMERATION_STATUS_CHOICES )
from django.db.models import Count, Avg
from django.contrib.auth.models import User
def report_year_range():
    this_year = datetime.date.today().year
    years = range(2005, this_year+1)
    return years


ENUMERATION_TYPE_WITH_ALL_CHOICES = [("ALL", "All"), ] +  list(ENUMERATION_TYPE_CHOICES)

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
    
    from_date         = forms.DateField(widget    = SelectDateWidget(
                                  years           = report_year_range()),
                                  initial         = datetime.date.today)
    
    status    = forms.ChoiceField(choices = ENUMERATION_STATUS_CHOICES,
                                    initial ="P")
                                    
    enumeration_type    = forms.ChoiceField(choices = ENUMERATION_TYPE_WITH_ALL_CHOICES,
                                    initial ="ALL")
    classification      = forms.ChoiceField(choices = ENUMERATION_CLASSIFICATION_CHOICES)
    mode                = forms.ChoiceField(choices = ENUMERATION_MODE_CHOICES)
        
    required_css_class  = 'required'
    
    def save(self):
        
        status = self.cleaned_data.get("status")
        enumeration_type = self.cleaned_data.get("enumeration_type")
        from_date = self.cleaned_data.get("from_date")
        classification = self.cleaned_data.get("classification")
        mode = self.cleaned_data.get("mode")
        
        if enumeration_type=="ALL":           
             #Create a query sett for all enumeration types.
             qs = GateKeeperError.objects.filter(
                    enumeration__mode = mode,
                    enumeration__status=status,
                    enumeration__classification = classification).exclude(added__gte=from_date)
                    
        else:
              qs = GateKeeperError.objects.filter(
                    enumeration__mode = mode,
                    enumeration__status = status,
                    enumeration__enumeration_type = enumeration_type,
                    enumeration__classification = classification).exclude(added__gte=from_date)
             

        #Get adisct list of all errors that are causing pending state.
        all_error_types   = qs.values_list('error_type').distinct()
         
        
        #built a list of lists to represent out output table
        results = []
        for et in all_error_types:
            row = []
            
            #create a new row starting with the error type
            row.append(et[0])
            
            # total ----------------------------------------------
            total = qs.filter(added__lte = from_date,
                              error_type = row[0]).count()
            row.append(total)
           
            # one  
            # create a date 1 days ago ---------------------------
            days_ago = from_date - datetime.timedelta(days=1)
            one_day   = qs.filter(added__gte=days_ago,
                                  added__lte = from_date,
                                  error_type = row[0]).count()
            
            row.append(one_day) 
            
            # 2-7 days ago ----------------------------------------
            days_ago_start = from_date - datetime.timedelta(days=7)
            days_ago_stop  = from_date - datetime.timedelta(days=2)
            
            two_to_seven  = qs.filter(added__gte=days_ago_start,
                                      added__lte =days_ago_stop,
                                      error_type = row[0]).count()
            
            row.append(two_to_seven)
            
            
            # 8-30 days ago ----------------------------------------
            days_ago_start = from_date - datetime.timedelta(days=30)
            days_ago_stop  = from_date - datetime.timedelta(days=8)            
            eight_to_thirty  = qs.filter(added__gte=days_ago_start,
                                      added__lte =days_ago_stop,
                                      error_type = row[0]).count()
            row.append(eight_to_thirty)
            
            
            # 30+ days ago -----------------------------------------
            days_ago_start = from_date - datetime.timedelta(days=30)         
            thirty_plus     = qs.filter(added__lte=days_ago_start,
                                      error_type = row[0]).count()
            row.append(thirty_plus)
            
            #Average -------------------------------------------------
            
            mydates  = qs.filter(added__lte = from_date,
                             error_type = row[0]).values_list('added')
            date_diff = []            
            for d in mydates:
                diff = from_date - d[0]
                date_diff.append(diff.days)
            
            average = sum(date_diff) / float(len(date_diff))
            
            row.append(average)
            #Append the row to results
            results.append(row)
            
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
        
        
        
        
         
    