#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.core.mail import EmailMessage,  EmailMultiAlternatives



def send_event_notification_email(event):
    subject = "[%s] %s" % (event.subject)    
    from_email = settings.EMAIL_HOST_USER
    to = event.enumeration.contact_person_email 
    headers = {'Reply-To': from_email}
    
    html_content = """
    <p>
    %s
    </p>
    <h1>Details</h1>
    <p>
    %s
    </p>
    <p>
    The NPPES Team @ CMS
    </p>
    """ % (event.enumeration.contact_person_first_name,
           event.enumeration.contact_person_last_name,
           event.body, event.details)
   
    text_content="""Hello: %s %s,
%s
    """ % (event.enumeration.contact_person_first_name,
           event.enumeration.contact_person_last_name,
           event.body
           )
    msg = EmailMultiAlternatives(subject, text_content, from_email,
                                 [to, ])
    msg.attach_alternative(html_content, "text/html")
    msg.send()