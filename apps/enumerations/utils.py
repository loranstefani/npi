#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings 
from django.http import Http404
import uuid, re

def get_enumeration_user_manages_or_404(Enumeration, enumeration_id, user):
    """
    Make sure the user has the right to mange this enumeration.
    Returns the enumeration object or raises 404.
    """
    
    #if user.is_staff==False:
    try:
        e = Enumeration.objects.select_related('managers').get(id=enumeration_id,
                                                               managers=user)
        return e
 
    except Enumeration.DoesNotExist:
        raise Http404('Not Found.')
    
    ##Else this is a staff user so let he or she continue.
    ##else
    #    try:
    #        e = Enumeration.objects.get(id=enumeration_id)
    #        return e
    # 
    #    except Enumeration.DoesNotExist:
    #        raise Http404('Not Found.')      



def valid_uuid(uuid):
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(str(uuid))
    return bool(match)