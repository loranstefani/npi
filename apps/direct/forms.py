from django import forms
from models import DirectAddress

class CreateDirectAddressForm(forms.ModelForm):
    
    class Meta:
        model =  DirectAddress
        fields = ('email', 'public', 'organization',)
    
   
    required_css_class = 'required'
