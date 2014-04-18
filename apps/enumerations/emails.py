#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives

def send_pending_email(enumeration):
    if enumeration.contact_person_email:
        subject = "[%s] Your NPI Enumeration is Pending" % (settings.ORGANIZATION_NAME)    
        from_email = settings.EMAIL_HOST_USER
        to = enumeration.contact_person_email.capitalize() 
        headers = {'Reply-To': from_email}
        
        html_content = """
        <p>
        Hello: %s %s,
        </p>
        <p>
        Your enumeration request is pending. More information may be required.
        </p>
        <p>
        Thank You,
        </p>
        <p>
        
        Centers for Medicare and Medicaid Services | Provider Enrollment Group
        </p>
        """ % (enumeration.contact_person_first_name.capitalize(),
               enumeration.contact_person_last_name.capitalize())
       
        text_content="""Hello: %s %s,
    Your enumeration request is pending. More information may be required.
    
    Thank You,
    
    Centers for Medicare and Medicaid Services | Provider Enrollment Group
        """ % (enumeration.contact_person_first_name.capitalize(),
               enumeration.contact_person_last_name.capitalize())
        msg = EmailMultiAlternatives(subject, text_content, from_email,
                                     [to, ])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        
def send_active_email(enumeration):
    if enumeration.contact_person_email:
        subject = "[%s] Your NPI Enumeration is Active" % (settings.ORGANIZATION_NAME)    
        from_email = settings.EMAIL_HOST_USER
        to = enumeration.contact_person_email.capitalize() 
        headers = {'Reply-To': from_email}
        
        html_content = """
        <p>
        Hello: %s %s,
        </p>
        <p>
        Congratulations. Your enumeration request complete and the enumeration
        is now active.  Your enumeration number is %s.
        </p>
        <p>
        Thank You,
        </p>
        <p>
        
        Centers for Medicare and Medicaid Services | Provider Enrollment Group
        </p>
        """ % (enumeration.contact_person_first_name.capitalize(),
               enumeration.contact_person_last_name.capitalize(),
               enumeration.number
               )
       
        text_content="""Hello: %s %s,
        
    Congratulations. Your enumeration request complete and the enumeration
    is now active.  Your enumeration number is %s.
    
    Thank You,
    
    Centers for Medicare and Medicaid Services | Provider Enrollment Group
        """ % (enumeration.contact_person_first_name.capitalize(),
               enumeration.contact_person_last_name.capitalize(),
               enumeration.number)
        msg = EmailMultiAlternatives(subject, text_content, from_email,
                                     [to, ])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
