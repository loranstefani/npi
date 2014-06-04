from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from forms import *
import json
from datetime import timedelta, date, datetime
from ..enumerations.models import Enumeration, Event, GateKeeperError
from ..taxonomy.models import TaxonomyCode



def api_view_enumeration(request, enumeration_number):
    pass

def api_enumeration_update(request):
    pass

def api_enumeration_create(request):
    pass




def events_since_date(request, date_start):
    #An empty list
    l =[]
    date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
    events = Event.objects.filter(updated__gte = date_start)
    
    for e in events:
        l.append(e.as_dict())
    
    l_json = json.dumps(l, indent =4 )
    
    return HttpResponse(l_json, mimetype="application/json")
    


