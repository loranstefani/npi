from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from models import Notification



@csrf_exempt
def sns_email_bounce(request):
    
    if request.method == 'POST':
        json_body = request.body
        
        regex = re.compile('^HTTP_')
        http_headers = dict((regex.sub('', header), value) for (header, value) 
            in request.META.items() if header.startswith('HTTP_'))
        n = Notification.objects.create(headers=http_headers, body = json_body)
        
        if not n.valid_json:
            print "Invalid json"
            return HttpResponse("Hello SNS Email Bounce (POST) Invalid JSON")
        print "Valid JSON"
        return HttpResponse("Hello SNS Email Bounce (POST) Valid JSON")
            
    #This is a GET
    return HttpResponse("Hello SNS Email Bounce (GET)")
        
        

def sns_email_complaint(request):
    pass

