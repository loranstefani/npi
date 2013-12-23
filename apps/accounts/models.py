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


CONTACT_CHOICES = ( ('sms','Send a text message to my mobile phone.'),
                    ('person-phone','Have someone call me.'),
                    ('email','Send me an email.'),
                    ('none','Do not send me a reminder.'),
                    )


TERM_CHOICES = ( (1,'1 Year'),
                 (3, '3 Year'),)


class Invitation(models.Model):
    code   = models.CharField(max_length = 10, unique=True)
    email  = models.EmailField(blank=True)
    valid = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.code
    
    def save(self, **kwargs):
        
         #send the verification email.
        msg = """
        <html>
        <head>
        </head>
        <body>
        Congratulations. You have been invited to join the NPPES Beta.<br>
        
        You may now register 
        <a href="http://npi.microehr.com/accounts/register">register</a>
        with the invitation code: 
        
        <h2>
        %s
        </h2>
        
        <p>
        NPPES is a site for managin provider enumerations.
        </p>
        </body>
        </html>
        """ % (self.code,)
        if settings.SEND_CA_EMAIL:
            subj = "[NPPES] Congratulations. Invitation Code: %s" % (self.code)
            
            msg = EmailMessage(subj, msg, settings.EMAIL_HOST_USER,
                           [self.email, ])            
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()

        super(Invitation, self).save(**kwargs)
        

class UserProfile(models.Model):
    user                        = models.ForeignKey(User, unique = True)
    invitation_code             = models.CharField(max_length = 20)
    date_of_birth               = models.DateField(auto_now_add=True)
    ssn                         = models.CharField(max_length = 20,
                                    verbose_name="Social Security Number")
    pin                         = models.CharField(max_length = 4,
                                                   blank = True, default = "")
    mobile_phone_number         = PhoneNumberField(max_length = 15,
                                                   blank = True)
    organization_name           = models.CharField(max_length = 256, blank=True)
    country                     = models.CharField(max_length = 2, default ="US")
    state                       = models.CharField(blank=True, max_length=2,
                                        choices=US_STATES,)
    city                        = models.CharField(max_length=256)
    
    preferred_language          = models.CharField( max_length = 2,
                                                   blank = True, default="en")
    npi                         = models.CharField(max_length=20,
                                                   default="", blank=True)
    email_verified              = models.BooleanField(default = False)
    sms_verified                = models.BooleanField(default = False)
    creation_date               = models.DateField(auto_now_add=True)


    def __unicode__(self):
        return '%s, %s (%s)' % (self.user.last_name, self.user.first_name,
                               self.user.username)


class ValidSignupKey(models.Model):
    user                 = models.ForeignKey(User)
    signup_key           = models.CharField(max_length=50, blank=True,
                                            unique=True)
    expires              = models.DateTimeField(default=datetime.now)
                           

    def __unicode__(self):
        return '%s for user %s expires at %s' % (self.signup_key,
                                                 self.user.username,
                                                 self.expires)
        
    def save(self, **kwargs):
        
        self.signup_key=str(uuid.uuid4())
        now = datetime.now()
        expires=now+timedelta(days=settings.SIGNUP_TIMEOUT_DAYS)
        self.expires=expires
        
        #send an email with reset url
        x=send_signup_key_via_email(self.user, self.signup_key)
        super(ValidSignupKey, self).save(**kwargs)


def validate_signup(signup_key):
    try:
        vc=ValidSignupKey.objects.get(signup_key=signup_key)
        now=datetime.now()
    
        if vc.expires < now:
            vc.delete()
            return False   
    except(ValidSignupKey.DoesNotExist):
        return False  
    u=vc.user
    u.is_active=True
    u.save()
    vc.delete()
    return True