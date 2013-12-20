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

from forms import SelectAddressTypeForm, DomesticAddressForm



#@login_required
def select_address_type(request):
    name = _("Create Address")
    if request.method == 'POST':
        form = SelectAddressTypeForm(request.POST)
        if form.is_valid():
            a = form.save()
            if a.address_type== "DOM":
                return HttpResponseRedirect(reverse('domestic_address', args=(a.id,)))
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
              'form': SelectAddressTypeForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))
    

def domestic_address(request, id):
    name = _("Domestic Address")
    if request.method == 'POST':
        form = DomesticAddressForm(request.POST)
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
              'form': DomesticAddressForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))

