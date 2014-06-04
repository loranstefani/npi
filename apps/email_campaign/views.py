from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re



@csrf_exempt
def sns_email_bounce(request):
    
    if request.method == 'POST':
        json_body = request.body
        
        regex = re.compile('^HTTP_')
        http_headers = dict((regex.sub('', header), value) for (header, value) 
            in request.META.items() if header.startswith('HTTP_'))
        
        
        print "Headers", http_headers
        print "Body", json_body
        
        try:
            new_body = json.loads(json_body)
            #load into SNS response into model
            
            
        except ValueError:
            return HttpResponse("Not JSON (POST)")
        
        return HttpResponse("Hello SNS Email Bounce (POST)")
            
    #This is a GET
    return HttpResponse("Hello SNS Email Bounce (GET)")
        
        

def sns_email_complaint(request):
    pass

