#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


from django import forms
from localflavor.us.us_states import US_STATES
from models import  Enumeration, License
import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from ..taxonomy.models import TaxonomyCode

SEARCH_US_STATES_CHOICES = [("", "No State"), ] + list(US_STATES)

from models import ENUMERATION_TYPE_CHOICES

def dob_range():
    this_year = datetime.date.today().year
    years = range(this_year-80, this_year-10)
    return years



class SelfTakeOverForm(forms.Form):
    provider_identifier  = forms.CharField(help_text ="""
                            Supply the nine digit provider identifier already assigned to you.""")
    year_of_birth        = forms.IntegerField()
    last_four_ssn        = forms.CharField(max_length=4, required=False)
    last_four_itin        = forms.CharField(max_length=4, required=False)
    i_attest             = forms.BooleanField(help_text ="""
                            I attest that this is me under the penalty of federal law.""")
    
    
    required_css_class = 'required'
    def clean(self):
        cleaned_data = super(SelfTakeOverForm, self).clean()

        
        #SSN and ITIN
        last_four_ssn = cleaned_data.get("last_four_ssn", "")
        last_four_itin = cleaned_data.get("last_four_itin", "")
        provider_identifier = cleaned_data.get("provider_identifier", "")
        year_of_birth= cleaned_data.get("year_of_birth", "")
        
        if not last_four_ssn and not last_four_itin:
            raise forms.ValidationError("You must provide either an SSN or an ITIN.")
        if  last_four_ssn and  last_four_itin:
            raise forms.ValidationError("You cannot proide both an SSN and an ITIN.")
            
        try:
            e = Enumeration.objects.get(number=provider_identifier)
        
        except Enumeration.DoesNotExist:
            raise forms.ValidationError("No provider identifer exists with that number.")
        #except:
        #    raise forms.ValidationError("No provider identifer exists with that number.")
        
        if last_four_ssn:
            print e.date_of_birth.year, e.ssn[-4:]
            if  last_four_ssn != e.ssn[-4:] or year_of_birth != e.date_of_birth.year:
                raise forms.ValidationError("This information cannot be verified.  Please call the help desk.")
       
        if last_four_itin:
            print e.date_of_birth.year, e.itin[-4:]
            if  last_four_itin != e.itin[-4:] or year_of_birth != e.date_of_birth.year:
                raise forms.ValidationError("This information cannot be verified.  Please call the help desk.")
       
        return cleaned_data
    
    def get_enumeration(self):
        number              = self.cleaned_data.get("provider_identifier", "")
        return Enumeration.objects.get(number=number)
        
        



class SearchForm(forms.ModelForm):
    class Meta:
        model = Enumeration
        fields = (
                  'number', 'first_name', 'last_name', 'organization_name',
                  'ein')

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



class DeactivateEnumerationForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(DeactivateEnumerationForm,self).__init__(*args,**kwargs)
        self.fields['flag_for_deactivation'].required = True
    class Meta:
        model = Enumeration
        fields = ('flag_for_deactivation', 'decativation_note',)
    required_css_class = 'required'




class DeactivationForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(DeactivationForm,self).__init__(*args,**kwargs)
        self.fields['deactivation_reason_code'].required = True
    class Meta:
        model = Enumeration
        fields = ('deactivation_reason_code','deactivated_details',)
    required_css_class = 'required'



class FraudAlertForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(FraudAlertForm,self).__init__(*args,**kwargs)
        self.fields['flag_for_fraud'].required = True
    class Meta:
        model = Enumeration
        fields = ('flag_for_fraud', 'fraud_alert_note',)
    required_css_class = 'required'



class SubmitApplicationForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(SubmitApplicationForm,self).__init__(*args,**kwargs)
        self.fields['confirmation'].required = True
    class Meta:
        model = Enumeration
        fields = ('confirmation', )
    required_css_class = 'required'




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

    class Meta:
        model = Enumeration
        fields = ('organization_name', 'ein', 'ein_image', 'doing_business_as')
    required_css_class = 'required'



class CreateEnumerationIndividualForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(CreateEnumerationIndividualForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['sole_proprietor'].required = True
        self.fields['sole_proprietor'].choices = (("", "No Answer"), ("YES", "Yes"),("NO", "No"))
        
    class Meta:
        model = Enumeration
        fields = ('name_prefix','first_name', 'last_name', 'name_suffix',
                  'sole_proprietor', 'doing_business_as', 'credential')

    required_css_class = 'required'
    



class IndividualPIIForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(IndividualPIIForm,self).__init__(*args,**kwargs)
        self.fields['state_of_birth'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['gender'].required = True
        self.fields['country_of_birth'].required = True

    class Meta:
        model = Enumeration
        fields = ('ssn', 'itin', 'itin_image', 'date_of_birth','state_of_birth',
                  'country_of_birth', 'gender', )


    required_css_class = 'required'
    
    def clean(self):
        cleaned_data = super(IndividualPIIForm, self).clean()

        
        #SSN and ITIN
        ssn = cleaned_data.get("ssn", "")
        itin = cleaned_data.get("itin", "")
        if not ssn and not itin:
            raise forms.ValidationError("You must provide an SSN or an ITIN.")
        if ssn and itin:
            raise forms.ValidationError("You cannot proide both an SSN and an ITIN.")
        
        #Country and state sanity check
        country_of_birth = cleaned_data.get("country_of_birth", "")
        state_of_birth   = cleaned_data.get("state_of_birth", "")
        if country_of_birth != "US" and state_of_birth != "ZZ":
            raise forms.ValidationError("You cannot be born in the United States and in a foreign country at the same time.")
        return cleaned_data




class OtherNamesForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(OtherNamesForm,self).__init__(*args,**kwargs)


    class Meta:
        model = Enumeration
        fields = ('other_name_code_1', 'other_first_name_1', 'other_middle_name_1',
                    'other_last_name_1',
                    'other_name_code_2',
                    'other_first_name_2', 'other_middle_name_1', 'other_last_name_2',
                    )


    required_css_class = 'required'




class ContactPersonForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(ContactPersonForm,self).__init__(*args,**kwargs)
        self.fields['contact_person_first_name'].required = True
        self.fields['contact_person_last_name'].required = True
        self.fields['contact_person_telephone_number'].required = True

    class Meta:
        model = Enumeration
        fields = ('contact_person_email',
                    'contact_person_prefix',
                    'contact_person_first_name',
                    'contact_person_middle_name',
                    'contact_person_last_name',
                    'contact_person_suffix', 'contact_person_title_or_position',
                    'contact_person_title_or_position',
                    'contact_person_telephone_number' ,
                    'contact_person_telephone_extension',
                    )


    required_css_class = 'required'





class AuthorizedOfficialForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(AuthorizedOfficialForm,self).__init__(*args,**kwargs)
        self.fields['authorized_official_first_name'].required = True
        self.fields['authorized_official_last_name'].required = True

    class Meta:
        model = Enumeration
        fields = (  'authorized_official_email', 'authorized_official_prefix',
                    'authorized_official_first_name',
                    'authorized_official_last_name',
                    'authorized_official_suffix', 'authorized_official_title_or_position',
                    'authorized_official_title_or_position',
                    'authorized_official_telephone_number' ,
                    'authorized_official_telephone_extension',
                    )


    required_css_class = 'required'



class PrimaryTaxonomyForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(PrimaryTaxonomyForm,self).__init__(*args,**kwargs)
        self.fields['taxonomy'].required = True


    class Meta:
        model = Enumeration
        fields = ('taxonomy',)


    required_css_class = 'required'



class PrimarySpecialtyForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        """Override the form's init"""
        super(PrimarySpecialtyForm,self).__init__(*args,**kwargs)
        self.fields['specialty'].required = True


    class Meta:
        model = Enumeration
        fields = ('specialty',)


    required_css_class = 'required'



class OtherTaxonomyForm(forms.ModelForm):

    #def __init__(self, *args,**kwargs):
    #    """Override the form's init"""
    #    super(OtherTaxonomyForm,self).__init__(*args,**kwargs)
    #    #self.fields['taxonomy'].required = True


    class Meta:
        model = Enumeration
        fields = ('other_taxonomies',)

    other_taxonomies = forms.ModelMultipleChoiceField(
                            queryset=TaxonomyCode.objects.all(),
                            widget=forms.CheckboxSelectMultiple(),
                            required=True)
    required_css_class = 'required'
    


class EnumerationEnhancementForm(forms.ModelForm):
    class Meta:
        model = Enumeration
        fields = ('handle', 'website', 'gravatar_email',
                  'facebook_handle','twitter_handle',
                  'driving_directions', 'bio_headline',)
    required_css_class = 'required'
    


class AddParentForm(forms.Form):
    number = forms.CharField(max_length=20, initial="", label="Number (e.g. NPI, OEID)")
    required_css_class = 'required'


