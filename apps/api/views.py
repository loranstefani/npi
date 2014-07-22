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
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from utils import get_unauthenticated_response


@csrf_exempt
def api_enumeration_write(request):
    if request.method == 'POST':
        unauthenticated_response  = get_unauthenticated_response(request)
        if unauthenticated_response :
            return unauthenticated_response 
       
        form = ProviderJSONForm(request.POST)
        if form.is_valid():
            validation_errors = form.validate()
            provider_write_response = {
                      "code": 400,
                      "message": "Enumeration create/update failed.",
                      "errors": validation_errors }
            if validation_errors:
                provider_write_response = {"errors": validation_errors }
                return HttpResponse(json.dumps(provider_write_response, indent =4),
                                           mimetype="application/json")
            else:
                save_response = form.save()
                return HttpResponse(json.dumps(save_response, indent =4),
                                           mimetype="application/json")
               
        else:
            errors=[]
            for k,v in form._errors.items():
                errors.append(v)
            jsonstr={"code": 400,
                      "message": "Enumeration create/update failed.",
                         "errors": errors }
            jsonstr=json.dumps(jsonstr, indent = 4,)
            return HttpResponse(jsonstr, mimetype="application/json") 
            
            
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
    


