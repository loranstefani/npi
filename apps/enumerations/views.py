from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from models import Enumeration
from ..addresses.models import Address
from ..licenses.models import License
import sys
from forms import *
from ..addresses.forms import *
from utils import get_enumeration_user_manages_or_404
from ..surrogates.models import Surrogate, SurrogateRequest


def search_enumeration(request):
    name = _("Search")
    if request.method == 'POST':
    
        form = SearchForm(request.POST,)
        
        if form.is_valid():
            qs = form.save()
            context= {'name':name,
                      'search_results': qs,
              'form': SearchForm()}
            return render_to_response('search.html',
                              RequestContext(request, context,))

        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,},
                                            RequestContext(request))
            
    #this is a GET
    context= {'name':name,
              'form': SearchForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))



@login_required
def surrogate_lookup(request):
    name = _("Search")
    if request.method == 'POST':
    
        form = SearchForm(request.POST,)
        
        if form.is_valid():
            qs = form.save()
            context= {'name':name,
                      'search_results': qs,
              'form': SearchForm()}
            return render_to_response('surrogate-request.html',
                              RequestContext(request, context,))

        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,},
                                            RequestContext(request))
            
    #this is a GET
    context= {'name':name,
              'form': SearchForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))

@login_required
def request_to_manage_enumeration(request, id):
    e = get_object_or_404(Enumeration, id=id)
    
    #Send an email to the authorized contact by reating a Surrogate Request
    sr = surrogateRequest.object.create(user=request.user, enumeration=e)
    #Add the enumeration to request.user's surrogate list
    s = Surrogate.objects.get(user=request.user)      
    s.enumerations.add(e)
    s.save()
    msg = _("Your request to manage enumeration was sent to the authorized official") 
    messages.success(request, msg)
    return HttpResponseRedirect(reverse('home'))


@login_required
def create_enumeration(request):
    name = _("Create New Entity for Enumeration")
    if request.method == 'POST':
        
        
        form = CreateEnumeration1Form(request.POST, mymanager=request.user.email)
        
        if form.is_valid():
            e = form.save(commit=False)
            e.contact_person_first_name     = request.user.first_name
            e.contact_person_last_name      = request.user.last_name
            e.contact_person_email          = request.user.email
            e.save()
            form.save_m2m()

           
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
def edit_basic_enumeration(request, id):
    name = _("Edit basic information for an enumeration")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    if e.enumeration_type in ("NPI-1", "OEID-1"):
        return HttpResponseRedirect(reverse('edit_individual_enumeration',
                                                   args=(e.id,)))
    else:
        return HttpResponseRedirect(reverse('edit_organization_enumeration',
                                                   args=(e.id,)))




@login_required
def create_individual_enumeration(request, id):
    name = _("Create a New Individual")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    
    
    if request.method == 'POST':
        form = CreateEnumerationIndividualForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save()
            
            return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
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
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    
    
    if request.method == 'POST':
        form = CreateEnumerationOrganizationForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save()
            return HttpResponseRedirect(reverse('edit_enumeration',
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
    
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user) 
    #this is a GET
    context= {'name': name,
              'enumeration': e,
              #'form': AdditionalInformationForm(instance=e)
              }
    return render_to_response('edit.html',
                              RequestContext(request, context,))




@login_required
def edit_enhanced_enumeration(request, id):
    name = _("Edit Enhanced Profile Information")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    
    
    if request.method == 'POST':
        form = EnumerationEnhancementForm(request.POST, request.FILES, instance=e)
        print "here"
        if form.is_valid():
            e = form.save()
            return HttpResponseRedirect(reverse('edit_enumeration',
                                                   args=(e.id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,'name':name,},
                                            RequestContext(request))
    #this is a GET
    context= {'name':name,
              'form': EnumerationEnhancementForm(instance=e)}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))




@login_required
def stop_managing_enumeration(request, enumeration_id):
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    e.managers.remove(e)
    s = Surrogate.objects.get(user=request.user)
    s.enumerations.remove(e)
    msg = _("You are no longer managing.")
    messages.error(request,msg)
    return HttpResponseRedirect(reverse('home',))
    
    




@login_required
def select_address_type(request, address_purpose, enumeration_id):
    name = _("Create Address")
    if request.method == 'POST':
        form = SelectAddressPurposeForm(request.POST,
                                        address_purpose=address_purpose)
        if form.is_valid():
            a = form.save()
            
            #save this address to the enumeration.
            e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                                    request.user)


            if str(address_purpose) == "LOCATION":
                e.location_address = a
                
            if str(address_purpose) == "MAILING":
                e.mailing_address = a
                
            if str(address_purpose) == "MEDREC-STORAGE":
                e.medical_record_storage_address = a
    
            if str(address_purpose) == "1099":
                e.ten_ninety_nine_address = a
                
            if str(address_purpose) == "REVALIDATION":
                e.revalidation_address = a
                        
            
            if str(address_purpose) in ("OTHER", "ADDITIONAL-LOCATION",):
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
              'form': SelectAddressPurposeForm(address_purpose=address_purpose)}
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
                                            args=(a.id,enumeration_id)))
    elif a.address_type == "MIL":
        return HttpResponseRedirect(reverse('military_address',
                                            args=(a.id,enumeration_id)))
    
    
    context= {'name':name,
              'form': SelectAddressTypeForm(instance=a)}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))
   



@login_required
def domestic_address(request,  address_id, enumeration_id):
    name = _("Domestic Address")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
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
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
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
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        form = MilitaryAddressForm(request.POST, instance=address)
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
              'form': MilitaryAddressForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))


