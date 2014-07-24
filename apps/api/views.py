from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
import json
from datetime import timedelta, date, datetime
from ..enumerations.models import Event
from django.views.decorators.csrf import csrf_exempt
from utils import get_unauthenticated_response, save_api_enumeration, validate


@csrf_exempt
def api_enumeration_write(request):
    if request.method == 'POST':
        unauthenticated_response  = get_unauthenticated_response(request)
        if unauthenticated_response :
            return unauthenticated_response 
        
        validation_errors = validate(request.body)
            
        if validation_errors:
            provider_write_response = {
                  "code": 400,
                  "status": "ERROR",
                  "message": "Enumeration create/update failed.",
                  "errors": validation_errors }
            return HttpResponse(json.dumps(provider_write_response, indent =4),
                                       content_type="application/json")
        else:
            save_response = save_api_enumeration(request)
            return HttpResponse(json.dumps(save_response, indent =4),
                                       content_type="application/json")
            
    
    #this is a GET
    provider_write_response = {
        "code": 200,
        "message": "POST Provider JSON to this URL to use the API. See https://github.com/HHSIDEAlab/pjson for details",}  
    return HttpResponse(json.dumps(provider_write_response, indent =4),
                                    content_type="application/json")
        


def events_since_date(request, date_start):
    #An empty list
    l =[]
    date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
    events = Event.objects.filter(updated__gte = date_start)
    
    for e in events:
        l.append(e.as_dict())
    
    l_json = json.dumps(l, indent =4 )
    
    return HttpResponse(l_json, content_type="application/json")
    


