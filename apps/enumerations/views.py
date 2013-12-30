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
from ..surrogates.models import Surrogate

@login_required
def create_enumeration(request):
    name = _("Create New Entity for Enumeration")
    if request.method == 'POST':
        
        
        form = CreateEnumeration1Form(request.POST, mymanager=request.user.email)
        
        if form.is_valid():
            e = form.save()
           
            #make sure this user is also the surrogate

            s = Surrogate.objects.get(user=request.user)
            
            s.enumerations.add(e)
            s.save()
            
            
           
            if e.enumeration_type in ("NPI-1", "OEID-1"):
               return HttpResponseRedirect(reverse('create_individual_enumeration',
                                                   args=(e.id,)))
            else:
                return HttpResponseRedirect(reverse('create_organization_enumeration',
                                                   args=(e.id,)))
            
        else:
            #The form is invalid
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


@login_required
def create_individual_enumeration(request, id):
    name = _("Create a New Individual")
    e = Enumeration.objects.get(id=id)
    
    
    if request.method == 'POST':
        form = CreateEnumerationIndividualForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save()
            
            return HttpResponseRedirect(reverse('select_address_type', args=(id,)))
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


@login_required
def create_organization_enumeration(request, id):
    name = _("Create a New Organization")
    e = Enumeration.objects.get(id=id)
    
    
    if request.method == 'POST':
        form = CreateEnumerationOrganizationForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save()
            return HttpResponseRedirect(reverse('select_address_type',
                                                   args=(e.id,)))
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

@login_required
def edit_enumeration(request, id):
    name = _("Edit Enumeration")
    e = Enumeration.objects.get(id=id)
    if request.method == 'POST':
        form = AdditionalInformationForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save()
            return enumeration_edit(id)
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('edit.html',
                                            {'form': form,'name':name,},
                                            RequestContext(request))
    #this is a GET
    context= {'name': name,
              'enumeration': e,
              'form': AdditionalInformationForm(instance=e)}
    return render_to_response('edit.html',
                              RequestContext(request, context,))




@login_required
def stop_managing_enumeration(request, enumeration_id):
    e = Enumeration.objects.get(id=enumeration_id)
    e.managers.remove(e)
    s = Surrogate.objects.get(user=request.user)
    s.enumerations.remove(e)
    msg = _("You are no longer managing.")
    messages.error(request,msg)
    return HttpResponseRedirect(reverse('home',))
    
    



@login_required
def select_address_type(request, enumeration_id):
    name = _("Create Address")
    if request.method == 'POST':
        form = SelectAddressTypeForm(request.POST)
        if form.is_valid():
            a = form.save()
            
            #save this address to the enumeration.
            e = Enumeration.objects.get(id=enumeration_id)
            print "Address Purposes",  a.address_purpose
            
            
#            ("PRIMARY-LOCATION",   
#("PRIMAY-BUSINESS",    
#("MEDREC-STORAGE",     
#("1099",               
#("REVALIDATION",       
#("ADDITIONAL-PRACTICE",
#("ADDITIONAL-BUSINESS",

            
            if str(a.address_purpose) == "PRIMARY-LOCATION":
                e.primary_practice_address = a
                
            if str(a.address_purpose) == "PRIMARY-BUSINESS":
                print "here"
                e.primary_business_address = a
            
            if a.address_purpose in ("ADDITIONAL-PRACTICE", "ADDITIONAL-BUSINESS"):
                e.other_addresses.add(a)
            
            e.save()


            if a.address_type == "DOM":
                return HttpResponseRedirect(reverse('domestic_address',
                                                    args=(a.id, e.id)))
            elif a.address_type == "FGN":
                return HttpResponseRedirect(reverse('foreign_address',
                                                    args=(a.id,e.id, )))
            elif a.address_type == "MIL":
                return HttpResponseRedirect(reverse('military_address',
                                                    args=(a.id,e.id, )))
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




@login_required
def edit_address(request, address_id, enumeration_id):
    a = Address.objects.get(id=address_id)
    name = _("Edit Address")
    
    if a.address_type == "DOM":
        return HttpResponseRedirect(reverse('domestic_address',
                                            args=(a.id,enumeration_id)))
    elif a.address_type == "FGN":
        return HttpResponseRedirect(reverse('foreign_address',
                                            args=(a.id,e.enumeration_id)))
    elif a.address_type == "MIL":
        return HttpResponseRedirect(reverse('military_address',
                                            args=(a.id,e.enumeration_id)))
    
    
    context= {'name':name,
              'form': SelectAddressTypeForm(instance=a)}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))
   


@login_required
def domestic_address(request,  address_id, enumeration_id):
    name = _("Domestic Address")
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        form = DomesticAddressForm(request.POST, instance=address)
        if form.is_valid():
            a = form.save()
            #based on address_purpose, 
            
            return HttpResponseRedirect(reverse('edit_enumeration',
                                    args=(enumeration_id )))
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
              'form': DomesticAddressForm(instance=address)}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))
    
    

@login_required
def foreign_address(request, address_id, enumeration_id):
    name = _("Foreign Address")
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        form = ForeignAddressForm(request.POST, instance=address)
        if form.is_valid():
            a = form.save()
            return HttpResponseRedirect(reverse('edit_enumeration',
                                    args=(enumeration_id )))
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
              'form': ForeignAddressForm(instance=address)}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))

@login_required
def military_address(request, address_id, enumeration_id):
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


