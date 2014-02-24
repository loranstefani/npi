#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ..enumerations.models import Enumeration
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
import uuid

class Surrogate(models.Model):
    """This model defines which enumerations are displayed in authenticaed home
    Creating this record does not confirm the surrogate relationship. It only
    is an attempted/requested surrogate relationship. To actually mananage the
    enumeration, the user must be added as a manager on the enumeration model
    """
    user           = models.ForeignKey(User, unique=True,db_index=True)
    enumerations   = models.ManyToManyField(Enumeration, null=True, blank=True, db_index=True)
  
    
    def __unicode__(self):
        #enumerations = ", ".join([enumeration.name for enumeration in self.enumerations.all()])

        s ="Surrogate:%s" % (self.user, )
        return s
    
class SurrogateRequestEnumeration(models.Model):
    """This model defines which enumerations are displayed in authenticaed home
    Creating this record does not confirm the surrogate relationship. It only
    is an attempted/requested surrogate relationship. To actually mananage the
    enumeration, the user must be added as a manager on the enumeration model
    """
    user                = models.ForeignKey(User, db_index=True)
    enumeration         = models.ForeignKey(Enumeration)
    key                 = models.CharField(max_length=50, blank=True, db_index=True)
    added               = models.DateField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    
    
    
    def __unicode__(self):
        s ="%s requests to manage %s" % (self.user,  self.enumeration)
        return s
    
    def save(self, **kwargs):
        if not self.key:
            self.key=str(uuid.uuid4())
        
        #send an email with reset url
        if settings.SEND_EMAIL:
            x=send_email_to_authorized_offical_to_manage_enumeration(self)
        super(SurrogateRequestEnumeration, self).save(**kwargs)
        
      
      
      
class SurrogateRequestEIN(models.Model):
    """This model defines which enumerations are displayed in authenticaed home
    Creating this record does not confirm the surrogate relationship. It only
    is an attempted/requested surrogate relationship. To actually mananage the
    enumeration, the user must be added as a manager on the enumeration model
    """
    user                = models.ForeignKey(User, db_index=True)
    ein                 = models.CharField(max_length=10, db_index=True)
    key                 = models.CharField(max_length=50, blank=True, db_index=True)
    added               = models.DateField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    
    
    
    def __unicode__(self):
        s ="%s requests to manage %s" % (self.user,  self.ein)
        return s
    
    def save(self, **kwargs):
        if not self.key:
            self.key=str(uuid.uuid4())
        
        #send an email with reset url
        if settings.SEND_EMAIL:
            enumerations =Enumeration.objects.filter(ein=self.ein)
            for e in enumerations:
                x=send_email_to_authorized_offical_to_manage_ein(self, e)
        super(SurrogateRequestEIN, self).save(**kwargs)  
        


def send_email_to_authorized_offical_to_manage_enumeration(surrogate_request_enumeration):
        
    grant_url = "%s/surrogates/grant-management-enumeration/%s" % (settings.HOSTNAME_URL,
                                                       surrogate_request_enumeration.key)
    
    html_content = """
        <html>
        <head>
        </head>
        <body>
        Hello %s %s.  %s %s (%s) has requested to manage the enumeration %s.
        You are on file as the authorized official for this enumeration, hence      
        you may grant this request by clicking on the following link. 
        <br>
        
   
        <a href="%s">Click here to grant management of this enumeration.</a>

        </body>
        </html>
        """ % (surrogate_request_enumeration.enumeration.authorized_person_first_name,
               surrogate_request_enumeration.enumeration.authorized_person_last_name,
               surrogate_request_enumeration.user.first_name,
               surrogate_request_enumeration.user.last_name,
               surrogate_request_enumeration.user.email,
               surrogate_request_enumeration.enumeration,
               grant_url)
        

    text_content = """
        Hello %s %s.  %s %s (%s) has requested to manage the enumeration %s.
        You are on file as the authorized official for this enumeration, hence      
        you may grant this request by clicking on the following link. 
        
        %s
        """ % (surrogate_request_enumeration.enumeration.authorized_person_first_name,
               surrogate_request_enumeration.enumeration.authorized_person_last_name,
               surrogate_request_enumeration.user.first_name,
               surrogate_request_enumeration.user.last_name,
               surrogate_request_enumeration.user.email,
               surrogate_request_enumeration.enumeration,
               grant_url)
        


    if settings.SEND_EMAIL:
            subj = "[NPPES] Request to Manage %s" % (surrogate_request_enumeration.enumeration)
            to = surrogate_request_enumeration.enumeration.authorized_person_email
            #print "SENTO", to
            
            
            msg = EmailMultiAlternatives(subj, text_content,
                                         settings.EMAIL_HOST_USER,[to,])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
    print "Email sent"
            
            

def send_email_to_authorized_offical_to_manage_ein(surrogate_request_ein, enumeration):
        
    grant_url = "%s/surrogates/grant-management-ein/%s" % (settings.HOSTNAME_URL,
                                                       surrogate_request_ein.key)
    
    html_content = """
        <html>
        <head>
        </head>
        <body>
        Hello %s %s.  %s %s (%s) has requested to manage all enumerations for
        the employee identification number (EIN) %s.
        You are on file as the authorized official for the enumeration %s, hence      
        you may grant this request by clicking on the following link. 
        <br>
        
   
        <a href="%s">Click here to grant management of this enumeration.</a>

        </body>
        </html>
        """ % (enumeration.authorized_person_first_name,
               enumeration.authorized_person_last_name,
               surrogate_request_ein.user.first_name,
               surrogate_request_ein.user.last_name,
               surrogate_request_ein.user.email,
               enumeration.ein,
               enumeration,
               grant_url)
        

    text_content = """
        Hello %s %s.  %s %s (%s) has requested to manage all enumerations for
        the employee identification number (EIN) %s.
        You are on file as the authorized official for the enumeration %s, hence      
        you may grant this request by clicking on the following link. 
        
        %s
        """ % (enumeration.authorized_person_first_name,
               enumeration.authorized_person_last_name,
               surrogate_request_ein.user.first_name,
               surrogate_request_ein.user.last_name,
               surrogate_request_ein.user.email,
               enumeration.ein,
               enumeration,
               grant_url)
        


    if settings.SEND_EMAIL:
        subj = "[NPPES] Request to Manage %s" % (enumeration)
        to = enumeration.authorized_person_email
        print "SENTO", to, "FOR", enumeration.number
            
            
        msg = EmailMultiAlternatives(subj, text_content,
                                 settings.EMAIL_HOST_USER,[to,])
        msg.attach_alternative(html_content, "text/html")
        msg.send()