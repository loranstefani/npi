from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from forms import ProviderJSONForm
import json
from datetime import timedelta, date, datetime
from ..enumerations.models import Enumeration, Event, GateKeeperError




def api_enumeration_write(request):
    if request.method == 'POST':
        form = ProviderJSONForm(request.POST)
        if form.is_valid():
            provider_write_response = form.save()
            provider_write_response = {"errors": [] }
            return HttpResponse(json.dumps(provider_write_response, indent =4),
                                           mimetype="application/json")
        else:
            provider_write_response = form.save()
            provider_write_response = {"errors": [] }
            return HttpResponse(json.dumps(provider_write_response, indent =4),
                                mimetype="application/json") 
    
    #this is a GET
    context =  {'form': ProviderJSONForm() }
    return render(request, 'generic/bootstrapform.html', context)





def events_since_date(request, date_start):
    #An empty list
    l =[]
    date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
    events = Event.objects.filter(updated__gte = date_start)
    
    for e in events:
        l.append(e.as_dict())
    
    l_json = json.dumps(l, indent =4 )
    
    return HttpResponse(l_json, mimetype="application/json")
    


