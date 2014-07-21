"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings



class SelfTakeover_TestCase(TestCase):
    "A user shall be able to take control (i.e. manage) of his or her own \
    type-1 NPI by providing some information and attesting it is indeed thier \
    information."
    
    
    fixtures=['test_enumeration_self_takeover.json']
    def setUp(self):
        
        self.client=Client()
        self.client.login(username="alan",
                          password="p")
        self.url=reverse('enmeration_self_take_over')
        
    
    
    def test_a_user_self_takeover_with_ssn(self):
        "Test a user shall be able to take control (i.e. manage) of his or her \
       own type-1 NPI by providing SSN and some information and attesting it is \
       indeed thier information."
        
        self.dict = {"provider_identifier":"197336268",
                    "year_of_birth": "1970",      
                    "last_four_ssn": "2222",           
                    "i_attest": True}
        response = self.client.post(self.url, self.dict, follow=True)
                
        # Check some response details
        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, "You are now in control of your own record.")
        
        
        

    def test_a_user_self_takeover_with_itin(self):
        "Test a user shall be able to take control (i.e. manage) of his or her \
       own type-1 NPI by providing ITIN and some information and attesting it is \
       indeed thier information."
        
        self.dict = {"provider_identifier":"131121552",
                    "year_of_birth": "1970",      
                    "last_four_itin": "8888",           
                    "i_attest": True}
        response = self.client.post(self.url, self.dict, follow=True)
                
        # Check some response details
        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, "You are now in control of your own record.")


    def test_a_user_self_takeover_with_invalid_last_four_ssn(self):
        "Test that a user supplying an incorrect last 4 SSN does not succeed self takeover"
        self.dict = {"provider_identifier":"197336268",
                    "year_of_birth": "1970",      
                    "last_four_ssn": "1111",           
                    "i_attest": True}
        response = self.client.post(self.url, self.dict)
                
        # Check some response details
        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, "This information cannot be verified")

    def test_a_user_self_takeover_with_invalid_last_four_itin(self):
        "Test that a user supplying an incorrect last 4 ITIN does not succeed self takeover"
        self.dict = {"provider_identifier":"131121552",
                    "year_of_birth": "1970",      
                    "last_four_itin": "1111",           
                    "i_attest": True}
        response = self.client.post(self.url, self.dict)
                
        # Check some response details
        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, "This information cannot be verified")


    def test_a_user_self_takeover_with_invalid_year_of_birth(self):
        "Test that a user supplying an incorrect year of birth does not succeed self takeover"
        self.dict = {"provider_identifier":"197336268",
                    "year_of_birth": "1971",      
                    "last_four_ssn": "2222",           
                    "i_attest": True}
        response = self.client.post(self.url, self.dict)
                
        # Check some response details
        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, "This information cannot be verified")
        

    def test_a_user_self_takeover_invalid_with_both_itin_and_ssn(self):
        "Test that a user supplying both ITIN and SSN does not succeed in self takeover"
        
        self.dict = {"provider_identifier":"197336268",
                    "year_of_birth": "1970",      
                    "last_four_ssn": "2222",
                    "last_four_itin": "8888",   
                    "i_attest": True}
        response = self.client.post(self.url, self.dict)
                
        # Check some response details
        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, "You cannot provide both an SSN and an ITIN")
        
    def test_a_user_self_takeover_invalid_without_attestation(self):
        "Test that when i_attest is False (uncheked) then self takeover fails."
        
        self.dict = {"provider_identifier":"197336268",
                    "year_of_birth": "1970",      
                    "last_four_ssn": "2222",
                    "i_attest": False}
        response = self.client.post(self.url, self.dict)
                
        # Check some response details
        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, "This field is required.")