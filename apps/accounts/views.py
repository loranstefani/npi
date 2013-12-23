#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db.models import Sum
from models import *
from forms import *
from django.core.urlresolvers import reverse
from utils import verify
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from models import ValidPasswordResetKey
from datetime import datetime
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


def mylogout(request):
    logout(request)
    messages.success(request, _("Logged out successfully."))
    return HttpResponseRedirect(reverse('home'))

    
def simple_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=authenticate(username=username, password=password)
            
            if user is not None:

                if user.is_active:
                    login(request,user)
                    patient = user.get_profile()
                    messages.success(request, _("You have logged in successfully."))
                    return HttpResponseRedirect(reverse('home'))
                else:
                   messages.error(request,
                        _("Your account is inactive so you may not log in."))
                   return render_to_response('accounts/login.html',
                                            {'form': form},
                                            RequestContext(request))
            else:
                messages.error(request, _("Invalid username or password."))
                return render_to_response('accounts/login.html',
                                    {'form': form},
                                    RequestContext(request))

        else:
         return render_to_response('accounts/login.html',
                              RequestContext(request, {'form': form}))
    #this is a GET
    return render_to_response('accounts/login.html',
                              {'form': LoginForm()},
                              context_instance = RequestContext(request))




def reset_password(request, reset_password_key=None):
    try:
        vprk=ValidPasswordResetKey.objects.get(
                                        reset_password_key=reset_password_key)
        
    except:
        return render_to_response('accounts/invalid-key.html',
                              RequestContext(request,
                                             {}))
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            vprk.user.set_password(form.cleaned_data['password1'])
            vprk.user.save()
            vprk.delete()
            logout(request)
            return render_to_response('accounts/reset-password-success.html',
                              RequestContext(request,{}))
        else:
         return render_to_response('accounts/reset-password.html',
                        RequestContext(request, {'form': form,
                            'reset_password_key': reset_password_key}))  
        
    return render_to_response('accounts/reset-password.html',
                              RequestContext(request,
                                    {'form': PasswordResetForm(),
                                    'reset_password_key': reset_password_key}))
        






def password_reset_request(request):
    if request.method == 'POST':

        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            return render_to_response('accounts/password-reset-request.html',
                              RequestContext(request,
                                             {'form': form,
                                              }))
    else:
        return render_to_response('accounts/password-reset-request.html', 
                             {'form': PasswordResetRequestForm()},
                              context_instance = RequestContext(request))
    



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
          new_user = form.save()
          messages.success(request, _("Please check your email to verify your account before logging in."))
          return HttpResponseRedirect(reverse('login'))
        else:
            #return the bound form with errors
            return render_to_response('accounts/signup.html',
                                      RequestContext(request, {'form': form}))      
    else:  
       #this is an HTTP  GET
       return render_to_response('accounts/signup.html',
                                 RequestContext(request,
                                {'form': SignupForm()}))     


def verify_email(request, verification_key,
                 template_name='accounts/activate.html',
                 extra_context=None):
    verification_key = verification_key.lower() # Normalize before trying anything with it.
    account = verify(verification_key)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account},
                              context_instance=context)
    


@login_required
def account_settings(request):
    name = _("Account Settings")
    up = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #update the user info
            request.user.username       = data['username']
            request.user.email          = data['email'] 
            request.user.save()
            #update the user profile
            up.mobile_phone_number      = data['mobile_phone_number']
            up.city                     = data['city']
            up.state                    = data['state']
            up.npi                      = data['npi']
            up.organization_name        = data['organization_name']
            up.save()
            messages.success(request,'Your account settings have been updated.')  
            return render_to_response('generic/bootstrapform.html',
                            {'form': form,
                             'name': name,
                             },
                            RequestContext(request))
        else:
            #the form had errors
            return render_to_response('generic/bootstrapform.html',
                            {'form': form,
                             'name': name,
                             },
                            RequestContext(request))
               

    #this is an HTTP GET        
    return render_to_response('generic/bootstrapform.html',
        {'name': name, 'form': AccountSettingsForm(
                              initial={ 'username':  request.user.username,
                                'email':                    request.user.email,
                                'organization_name':        up.organization_name,
                                'last_name':                request.user.last_name,
                                'first_name':               request.user.first_name,
                                'mobile_phone_number':      up.mobile_phone_number,
                                'city':                     up.city,
                                'state':                    up.state,
                                'npi':                      up.npi,
                                 #'country':                up.mobile_phone_number,
                                })},
                              RequestContext(request))


def signup_verify(request, signup_key=None):
    
    if validate_signup(signup_key=signup_key):
        messages.success(request, "Your account has been activated. You may now login.")
        return HttpResponseRedirect(reverse('login'))
    else:
        return render_to_response('accounts/invalid-key.html',
                              RequestContext(request,
                                             {}))
    