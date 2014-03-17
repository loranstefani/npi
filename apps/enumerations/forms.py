#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


from django import forms
from localflavor.us.us_states import US_STATES
from models import  Enumeration, License
import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

MY_US_STATES = [("", "No State"), ]

MY_US_STATES = MY_US_STATES + list(US_STATES)

from models import ENUMERATION_TYPE_CHOICES


class SearchForm(forms.ModelForm):
    class Meta:
        model = Enumeration
        fields = (
                  'number', 'first_name', 'last_name', 'organization_name',
                  'ein'
                  )
    
    city  = forms.CharField(required=False)
    state = forms.ChoiceField(choices=MY_US_STATES, required=False)
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
                                            **q)[:10]
        else:
            qs = Enumeration.objects.filter(**q)[:10]
        
        return qs
    
class SearchEINForm(forms.ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""     
        super(SearchEINForm,self).__init__(*args,**kwargs)
        self.fields['ein'].required = True    
    
    
    class Meta:
        model = Enumeration
        fields = ('ein',)
        
    required_css_class = 'required'
    
    def save(self, force_insert=False, force_update=False, commit=True):
        
        q={}
        ein                 = self.cleaned_data.get("ein", "")
        
        if ein:
            q['ein']=ein
            
        qs = Enumeration.objects.filter(**q)[:1000]
        return qs




class CreateEnumeration1Form(forms.ModelForm):
    
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
    
    
class CreateEnumeration2Form(forms.Form):
    enumeration_type = forms.ChoiceField(choices=ENUMERATION_TYPE_CHOICES)

    required_css_class = 'required'    
    

class CreateEnumerationOrganizationForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(CreateEnumerationOrganizationForm,self).__init__(*args,**kwargs)
        self.fields['organization_name'].required = True
        self.fields['ein'].required = True
        self.fields['ein'].help_text = "An EIN is issued by the IRS. This is required for organizations."
        #self.fields['contact_person_first_name'].required = True
        #self.fields['contact_person_last_name'].required = True
        #self.fields['contact_person_telephone_number'].required = True
        #self.fields['authorized_official_first_name'].required = True
        #self.fields['authorized_official_last_name'].required = True
        #self.fields['authorized_official_telephone_number'].required = True


        
    class Meta:
        model = Enumeration
        fields = ('organization_name', 'ein', 'ein_image', 'doing_business_as',
                    'contact_person_email', 'contact_person_first_name',
                    'contact_person_middle_name', 'contact_person_last_name',
                    'contact_person_suffix', 'contact_person_title_or_position',
                    'contact_person_title_or_position',
                    'contact_person_telephone_number' ,
                    'contact_person_telephone_extension',
                    'authorized_official_email', 'authorized_official_prefix',
                    'authorized_official_first_name',
                    'authorized_official_last_name',
                    'authorized_official_suffix', 'authorized_official_title_or_position',
                    'authorized_official_title_or_position',
                    'authorized_official_telephone_number' ,
                    'authorized_official_telephone_extension',
                  )
    required_css_class = 'required'
    


class CreateEnumerationIndividualForm(forms.ModelForm):
    
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(CreateEnumerationIndividualForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        #self.fields['contact_person_first_name'].required = True
        #self.fields['contact_person_last_name'].required = True
        #self.fields['contact_person_telephone_number'].required = True
        #self.fields['authorized_person_first_name'].required = True
        #self.fields['authorized_person_last_name'].required = True
        #self.fields['authorized_person_telephone_number'].required = True
        #self.fields['ssn'].required = True
        
    class Meta:
        model = Enumeration
        fields = ('first_name', 'last_name', 'ssn', 'itin',
                'state_of_birth','country_of_birth',
                  'birth_date', 'gender',
                  'sole_proprietor',
                  'doing_business_as',
                    'contact_person_email', 'contact_person_first_name',
                    'contact_person_middle_name',
                    'contact_person_last_name',
                    'contact_person_suffix', 'contact_person_title_or_position',
                    'contact_person_title_or_position',
                    'contact_person_telephone_number' ,
                    'contact_person_telephone_extension',
                    #'authorized_official_email', 'authorized_official_prefix',
                    #'authorized_official_first_name',
                    #'authorized_official_last_name',
                    #'authorized_official_suffix', 'authorized_official_title_or_position',
                    #'authorized_official_title_or_position',
                    #'authorized_official_telephone_number' ,
                    #'authorized_official_telephone_extension',
                    'other_name_code_1', 'other_first_name_1', 'other_middle_name_1',          
                    'other_last_name_1',
                    'other_name_code_2',
                    'other_first_name_2', 'other_middle_name_1', 'other_last_name_2',
                    )
        
    required_css_class = 'required'


class EnumerationEnhancementForm(forms.ModelForm):
    class Meta:
        model = Enumeration
        fields = ('custom_profile_url', 'website', 'facebook_handle',
                  'twitter_handle', 'driving_directions', 'bio_headline',
                  'bio_detail', 'avatar_image', 'background_image',)
    required_css_class = 'required'



class AddParentForm(forms.Form):
    number = forms.CharField(max_length=20, initial="", label="Number (e.g. NPI, OEID)")
    required_css_class = 'required'


