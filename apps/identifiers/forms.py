from django import forms
from models import Identifier

class IdentifierForm(forms.ModelForm):
    
    class Meta:
        model =  Identifier
        fields = ('identifier', 'code', 'state', 'issuer',)

   
    required_css_class = 'required'
