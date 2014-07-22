#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.contrib.auth.models import User
import json, binascii
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

def get_unauthenticated_response(request):
    auth_string = request.META.get('HTTP_AUTHORIZATION', None)
    
    
    #if none then the user was authenticated.
    response = None 
    
    if not auth_string:
        jsonstr={"code": 401, "message": "No HTTP_AUTHORIZATION supplied."}
        jsonstr=json.dumps(jsonstr, indent = 4,)
        response = HttpResponse(jsonstr) 
    else:
    
    
        
        try:
            (authmeth, auth) = auth_string.split(" ", 1)
    
            if not authmeth.lower() == 'basic':
                jsonstr={"code": 401,
                          "message": "No HTTP_AUTHORIZATION supplied."}
                jsonstr=json.dumps(jsonstr, indent = 4,)
                response = HttpResponse(jsonstr, mimetype="application/json")
    
            
            #information was supplied
            auth = auth.strip().decode('base64')
            (username, password) = auth.split(':', 1)
            #authenticate
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    #the account is disabled
                    jsonstr={"code": 401, "message": "Account disabled."}
                    jsonstr=json.dumps(jsonstr, indent = 4,)
                    response =  HttpResponse(jsonstr, mimetype="application/json")
                else:
                    #login the user
                    login(request, user)
            else:
                # the authentication system was unable to verify the username and password
                jsonstr={"code": 401, "message": "Invalid username or password."}
                jsonstr=json.dumps(jsonstr, indent = 4,)
                response =  HttpResponse(jsonstr, mimetype="application/json")
            
        
        except (ValueError, binascii.Error):
            jsonstr={"code": 401, "message": "No HTTP_AUTHORIZATION supplied."}
            jsonstr=json.dumps(jsonstr, indent = 4,)
            response =  HttpResponse(jsonstr, mimetype="application/json")
    
    return response
    
     
       
    