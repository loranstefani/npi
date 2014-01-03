#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
 
from django.http import Http404
 
def get_enumeration_user_manages_or_404(Enumeration, enumeration_id, user):
    """
    Make sure the user has the right to mange this enumeration.
    Returns the enumeration object or raises 404.
    """
    try:
        e = Enumeration.objects.select_related('managers').get(id=enumeration_id,
                                                               managers=user)
        return e
 
    except Enumeration.DoesNotExist:
        raise Http404('Not Found.')
