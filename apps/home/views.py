from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _



def home(request):
    if request.user.is_authenticated():
        return authenticated_home(request)
    else:
       context ={}
       return render_to_response('home/index.html',
                              RequestContext(request, context,)) 


@login_required
def authenticated_home(request):
    name = "Page name"
    #this is a GET
    context= {'name':name,
              }
    return render_to_response('home/authenticated-home.html',
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


