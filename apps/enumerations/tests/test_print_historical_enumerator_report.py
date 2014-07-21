"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings



class PrintHistoricalReport_TestCase(TestCase):
    "Output an HTML report containing all historical report information"
    
    fixtures=['test_enumeration_self_takeover.json']
    
    def setUp(self):
        
        self.client=Client()
        self.client.login(username="alan",
                          password="p")
        self.url=reverse('enmeration_create_historical_report', args=("1",))
        


    def test_a_user_historical_report_is_not_accesible_by_non_staff(self):
        "accessing this URL without staff privilegaes redirect to staff login"
        self.client.login(username="not-staff",
                          password="p")
        response = self.client.get(self.url, {})
                
        # Check some response details
        self.assertEqual(response.status_code, 200)    


    
    def test_a_user_historical_report_is_generated(self):
        "supplying a valid enumeration number and having staff status results \
        in an HTML report"

        response = self.client.get(self.url, {})
                
        # Check some response details
        self.assertEqual(response.status_code, 200)
        

