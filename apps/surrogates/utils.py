#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _

def send_email_to_newly_authorized_manager(surrogate_request):
        
    html_content = """
        <html>
        <head>
        </head>
        <body>
        Hello %s %s.  %s %s (%s) has approved you management request for
        requested to manage the enumeration %s.  You may now login to NPPES
        and make updates and changes as necessary.
        </body>
        </html>
        """ % (surrogate_request.user.first_name,
               surrogate_request.user.last_name,
               surrogate_request.enumeration.contact_person_first_name,
               surrogate_request.enumeration.contact_person_last_name,
               surrogate_request.enumeration.contact_person_email,
               surrogate_request.enumeration)
        

    text_content = """
        Hello %s %s.  %s %s (%s) has approved you management request for
        requested to manage the enumeration %s.  You may now login to NPPES
        and make updates and changes as necessary.
        """ % (surrogate_request.user.first_name,
               surrogate_request.user.last_name,
               surrogate_request.enumeration.contact_person_first_name,
               surrogate_request.enumeration.contact_person_last_name,
               surrogate_request.enumeration.contact_person_email,
               surrogate_request.enumeration)
        


    if settings.SEND_EMAIL:
            subj = "[NPPES] Your Request to Manage %s has Been Approved" % (surrogate_request.enumeration)
            to = surrogate_request.user.email            
            msg = EmailMultiAlternatives(subj, text_content,
                                         settings.EMAIL_HOST_USER,[to,])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
           