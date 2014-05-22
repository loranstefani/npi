#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from models import DeceasedMasterFile
import os, uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from utils import valid_dmf


class DMFForm(forms.ModelForm):
    
    class Meta:
        model =  DeceasedMasterFile
        fields  = ('file', )
        
    def clean_file(self):
        file = self.cleaned_data.get('file', '')

        #check a file in form for viruses
        if file and settings.ANTI_VIRUS:
            from tempfile import mkstemp
            import pyclamd
            import os
            
            #Raise an error if ANTI_VIRUS server not reachable
            try:
                 cd = pyclamd.ClamdUnixSocket()
                 # test if server is reachable
                 cd.ping()
            except pyclamd.ConnectionError:
                 # if failed, test for network socket
                 cd = pyclamd.ClamdNetworkSocket()
                 try:
                     cd.ping()
                 except pyclamd.ConnectionError:
                     raise forms.ValidationError('Could not connect to clamd server either by unix or network socket.')
            
        #The AV is working so scan the file.
        
        #Create a temporary file name
        tmp_fn = str(uuid.uuid4())
        
        #get the data from the file.
        data = self.files['file']

        #Save the temp file.
        path = default_storage.save(tmp_fn, ContentFile(data.read()))
        
        #Uncommenting the next line will write a test virus instead of file in form. 
        #path = default_storage.save(tmp_fn, ContentFile(cd.EICAR()))
        
        tmp_path = str(os.path.join(settings.MEDIA_ROOT, path))
         
        #scan for viruses    
        if cd.scan_file(tmp_path) is not None:
            #A virus was found. 
            #Delete the tmp file
            os.remove(tmp_path)
            #Raise Validation Error
            raise forms.ValidationError("A virus was detected in this file and therefore it was rejected.")
            
        #remove the temp file since this is just a clean
        os.remove(tmp_path)       
    
        #Make sure the file is a valid SSA DMF
        if not valid_dmf(file):
            raise forms.ValidationError("The files does not appear to be a valid DMF.")
        
        
        
        
        return file