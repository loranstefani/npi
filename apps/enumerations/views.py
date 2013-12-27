from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from models import Address, Enumeration, License
import sys
from forms import *



@login_required
def create_enumeration(request):
    name = _("Create New Entity for Enumeration")
    if request.method == 'POST':
        
        
        form = CreateEnumeration1Form(request.POST, mymanager=request.user.email)
        
        if form.is_valid():
           e = form.save()
           #e.managers = request.user
           #e.save_m2m()
           if e.enumeration_type in ("NPI-1", "OEID-1"):
               return HttpResponseRedirect(reverse('create_individual_enumeration',
                                                   args=(e.id,)))
           else:
                return HttpResponseRedirect(reverse('create_organization_enumeration',
                                                   args=(e.id,)))
            
        else:
            #The form is invalid
             print "invalid form", form.is_bound(), form.errors
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,},
                                            RequestContext(request))
            
    #this is a GET
    context= {'name':name,
              'form': CreateEnumeration1Form(initial={"manager":request.user.email,},
                                             mymanager=request.user.email, 
                                             )}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))


def create_individual_enumeration(request, id):
    name = _("Create a New Individual")
    e = Enumeration.objects.get(id=id)
    
    
    if request.method == 'POST':
        form = CreateEnumerationIndividualForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save()
            return enumeration_edit(id)
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,'name':name,},
                                            RequestContext(request))
    #this is a GET
    context= {'name':name,
              'form': CreateEnumerationIndividualForm(instance=e)}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))

def create_organization_enumeration(request, id):
    name = _("Create a New Organization")
    e = Enumeration.objects.get(id=id)
    
    
    if request.method == 'POST':
        form = CreateEnumerationOrganizationForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save()
            return enumeration_edit(id)
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,'name':name,},
                                            RequestContext(request))
    #this is a GET
    context= {'name':name,
              'form': CreateEnumerationOrganizationForm(instance=e)}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))

def enumeration_edit(id):
    return HttpResponse("OK")


#@login_required
def select_address_type(request):
    name = _("Create Address")
    if request.method == 'POST':
        form = SelectAddressTypeForm(request.POST)
        if form.is_valid():
            a = form.save()
            if a.address_type == "DOM":
                return HttpResponseRedirect(reverse('domestic_address', args=(a.id,)))
            elif a.address_type == "FGN":
                return HttpResponseRedirect(reverse('foreign_address', args=(a.id,)))
            elif a.address_type == "MIL":
                return HttpResponseRedirect(reverse('military_address', args=(a.id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,'name':name,},
                                            RequestContext(request))
            
    #this is a GET
    context= {'name':name,
              'form': SelectAddressTypeForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))
    

def domestic_address(request, id):
    name = _("Domestic Address")
    if request.method == 'POST':
        form = DomesticAddressForm(request.POST)
        if form.is_valid():
            a = form.save()
            return HttpResponseRedirect(reverse('home',))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
    
    #this is a GET
    context= {'name':name,
              'form': DomesticAddressForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))
    
    
def foreign_address(request, id):
    name = _("Foreign Address")
    if request.method == 'POST':
        form = ForeignAddressForm(request.POST)
        if form.is_valid():
            a = form.save()
            if a.address_type== "DOM":
                return HttpResponseRedirect(reverse('home',))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
    
    #this is a GET
    context= {'name':name,
              'form': ForeignAddressForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))


def military_address(request, id):
    name = _("Military Address")
    if request.method == 'POST':
        form = MilitaryAddressForm(request.POST)
        if form.is_valid():
            a = form.save()
            if a.address_type== "DOM":
                return HttpResponseRedirect(reverse('home',))

        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,
                                             },
                                            RequestContext(request))
    
    #this is a GET
    context= {'name':name,
              'form': MilitaryAddressForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))


