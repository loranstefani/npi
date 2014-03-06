#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import json, sys
from django.conf import settings
from django.contrib.auth.models import User
import urllib,  urllib2, socket, base64, httplib

class IABackend(object):
    supports_anonymous_user=False
    supports_object_permissions=False
    
    def get_user(self, user_id):

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    def authenticate(self, username=None, password=None):
        
        #A header for HTTP POST
        http_header = {"Content-type": "application/x-www-form-urlencoded",}
        
        #POST parameters.
        params = {  "username":   username,
                    "password":    password,
                 }
        
        #set default timeout for HTTP connection.
        timeout = 15
        socket.setdefaulttimeout(timeout)
        
        # create your HTTP request
        req = urllib2.Request(settings.IA_AUTH_URL,
                              urllib.urlencode(params),
                              http_header)

        #build opener
        opener = urllib2.build_opener()
    
        try: 
            # submit your request
            res = opener.open(req)
            j = res.read()
            try:
                user = User.objects.get(username=username)
                #convert our happy response from JSON into a dict
                json_dict = json.loads(j)
                #Set additional info from response.
                user.first_name=json_dict["first_name"]
                user.last_name=json_dict["last_name"]
                user.email=json_dict["email"]
                #Save it
                user.save()
                #return the user
                return user
            except User.DoesNotExist:                
                #User does not exist but the user/pass is valid, so create the user.
                user = User(username=username, password=password)
                #set salted hashed password.
                user.set_password(password)
                #convert our happy response from JSON into a dict
                json_dict = json.loads(j)
                #Set additional info from response.
                user.first_name=json_dict["first_name"]
                user.last_name=json_dict["last_name"]
                user.email=json_dict["email"]
                #Save it
                user.save()
                #return the user
                return user            
    
        except urllib2.HTTPError, e:
            #print e.code
            #print e.read()
            #j = e.read()
            return None
            
           
        except urllib2.URLError, e:
            error = 'URLError = ' + str(e.reason)            
            r = {
                "code": 500,
                "errors":[ {"description":  error }, ]
                }
            #print r
            return None
            
        except httplib.HTTPException, e:
            error = "HTTPException = %s"  % (str(e))
            r = {
                "code": 500,
                "errors":
                      [
                        {"description":  error },
                        ]
                }
            #print r
            return None
            
        except Exception:
            
            r = {
                "code": 500,
                "errors": [
                        {"description":  str(sys.exc_info()[1]) },
                        ]
                }            
            #print r
            return None
