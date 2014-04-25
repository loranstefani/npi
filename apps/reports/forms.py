#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.forms.extras.widgets import SelectDateWidget
from localflavor.us.us_states import US_STATES
import datetime
from django import forms
from ..enumerations.models import (Enumeration, GateKeeperError,
                                   ENUMERATION_TYPE_CHOICES, 
                                   ENUMERATION_MODE_CHOICES,
                                   ENUMERATION_CLASSIFICATION_CHOICES,
                                   ENUMERATION_STATUS_CHOICES )
from django.db.models import Count, Avg
from django.contrib.auth.models import User


SEARCH_US_STATES_CHOICES = [("", "No State"), ] + list(US_STATES)

def report_year_range():
    this_year = datetime.date.today().year
    years = range(2005, this_year+1)
    return years


ENUMERATION_TYPE_WITH_ALL_CHOICES = [("ALL", "All"), ] +  list(ENUMERATION_TYPE_CHOICES)

def default_from_date(subtract_days=60):
    return datetime.date.today() - datetime.timedelta(days=subtract_days)




class ReportSearchForm(forms.ModelForm):
    class Meta:
        model = Enumeration
        fields = ( 'status', 'number', 'first_name', 'last_name',
                  'organization_name', 'ein', 'ssn', )

    city  = forms.CharField(required=False)
    state = forms.ChoiceField(choices=SEARCH_US_STATES_CHOICES, required=False)
    required_css_class = 'required'

    def save(self, force_insert=False, force_update=False, commit=True):

        q={}
        number              = self.cleaned_data.get("number", "")
        first_name          = self.cleaned_data.get("first_name", "")
        last_name           = self.cleaned_data.get("last_name", "")
        organization_name   = self.cleaned_data.get("organization_name", "")
        city                = self.cleaned_data.get("city", "")
        state               = self.cleaned_data.get("state", "")
        ein                 = self.cleaned_data.get("ein", "")
        ssn                 = self.cleaned_data.get("ssn", "")
        status              = self.cleaned_data.get("status", "")
        itin                = self.cleaned_data.get("itin", "")

        if status:
            q['status']=status
        if number:
            q['ssn']=ssn

        if number:
            q['number']=number.upper()

        if first_name:
            q['first_name']=first_name.upper()

        if last_name:
            q['last_name']=last_name.upper()

        if organization_name:
            q['organization_name']=organization_name.upper()


        if ein:
            q['ein']=ein

        if state and not city:

            qs = Enumeration.objects.filter(location_address__state=state.upper(), **q)[:10]

        elif state and city:
            qs = Enumeration.objects.filter(location_address__state=state.upper(),
                                            location_address__city=city.upper(),
                                            **q)[:5000]
        else:
            qs = Enumeration.objects.filter(**q)[:5000]

        return qs




class EnumerationApplicationForm(forms.Form):
    ENUMERATION_STATUS_CHOICES = (('P','Pending'), ('E','Editing'))
    status    = forms.ChoiceField(choices = ENUMERATION_STATUS_CHOICES,
                                    initial ="P")
    enumeration_type    = forms.ChoiceField(choices = ENUMERATION_TYPE_CHOICES)
    required_css_class  = 'required'
    
    def save(self):
         enumeration_type = self.cleaned_data.get("enumeration_type")
         status = self.cleaned_data.get("status")
         qs = Enumeration.objects.filter(status = status,
                                         enumeration_type = enumeration_type)
         return qs
        
        

class PendingEnumerationOverviewForm(forms.Form):
    from_date   = forms.DateField(widget    = SelectDateWidget(
                                  years           = report_year_range()),
                                  initial         = datetime.date.today)
    
    status      = forms.ChoiceField(choices = ENUMERATION_STATUS_CHOICES,
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
        
        
        
        
         
    