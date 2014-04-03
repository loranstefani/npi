#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from datetime import timedelta, date
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from localflavor.us.models import PhoneNumberField
from localflavor.us.us_states import US_STATES
from sms_utils import send_sms_twilio
import string
import random
import uuid
from emails import send_password_reset_url_via_email, send_signup_key_via_email
from django.core.mail import send_mail, EmailMessage
from django.utils.translation import ugettext_lazy as _



class RequestInvite(models.Model):
    first_name     = models.CharField(max_length = 150)
    last_name      = models.CharField(max_length = 150)
    organization   = models.CharField(max_length = 150)
    email          = models.EmailField(max_length = 150)
    added          = models.DateField(auto_now_add=True)
    def __unicode__(self):
        r = "%s %s" % (self.first_name, self.last_name)
        return r

class Invitation(models.Model):
    code   = models.CharField(max_length = 10, unique=True)
    email  = models.EmailField(blank=True)
    valid = models.BooleanField(default=True)
    added          = models.DateField(auto_now_add=True)
    
    
    def __unicode__(self):
        return self.code
    
    def save(self, **kwargs):
        
         #send the verification email.
        msg = """
        <html>
        <head>
        </head>
        <body>
        Congratulations. You have been invited to join the NPPES Alpha.<br>
        
        You may now <a href="%s">register</a>
        with the invitation code: 
        
        <h2>
        %s
        </h2>
        
        - NPPES Modernization Team 
        </body>
        </html>
        """ % (settings.HOSTNAME_URL, self.code,)
        if settings.SEND_EMAIL:
            subj = "[%s] Invitation Code: %s" % (settings.ORGANIZATION_NAME,
                                                    self.code)
            
            msg = EmailMessage(subj, msg, settings.EMAIL_HOST_USER,
                           [self.email, ])            
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()

        super(Invitation, self).save(**kwargs)
        
class ValidPasswordResetKey(models.Model):
    user               = models.ForeignKey(User)
    reset_password_key = models.CharField(max_length=50, blank=True)
    expires            = models.DateTimeField(default=datetime.now)


    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.reset_password_key,
                                                 self.user.username,
                                                 self.expires)

    def save(self, **kwargs):

        self.reset_password_key=str(uuid.uuid4())
        now = datetime.now()
        expires=now+timedelta(minutes=settings.SMS_LOGIN_TIMEOUT_MIN)
        self.expires=expires

        #send an email with reset url
        x=send_password_reset_url_via_email(self.user, self.reset_password_key)
        super(ValidPasswordResetKey, self).save(**kwargs)