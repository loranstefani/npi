"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings



class WriteAPI_TestCase(TestCase):
    "A user shall be able to create and/or update an NPI by uploading ProviderJSON"
    
    
    fixtures=['test_write_api.json']
    def setUp(self):
        
        self.client=Client()
        self.client.login(username="alan",
                          password="p")
        self.url=reverse('api_enumeration_write')
        
    
    
    def test_writeAPI_create_with_clean_providerJSON(self):
        "Test that an NPI is created when all necessary information is provided \
        in ProviderJSON format"
        
        self.dict = {"providerjson":"{}"}
        response = self.client.post(self.url, self.dict, follow=True)
                
        # Check some response details
        self.assertEqual(response.status_code, 200)        
        