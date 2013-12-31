from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import sys
from forms import *
from ..enumerations.models import Enumeration

@login_required
def novaladd_license(request, enumeration_id):
    name = _("Create License")
    if request.method == 'POST':
        form = CreateLicenseForm(request.POST)
        
        if form.is_valid():
            l = form.save()
            e = Enumeration.objects.get(id=enumeration_id)
            e.licenses.add(l)
            e.save()
            return HttpResponseRedirect(reverse('edit_enumeration',
                                                   args=(enumeration_id,)))
            
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                             'name':name,},
                                            RequestContext(request))
            
    #this is a GET
    context= {'name':name,
              'form': CreateLicenseForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))


@login_required
def add_license(request, enumeration_id):
    name = _("Add a Medical License Automatically")
    if request.method == 'POST':
        form = AutoVerifyLicenseForm(request.POST)
        
        if form.is_valid():
            l = form.save(commit=False)
            l.verified_by_issuing_board = True
            l.save()
            
            e = Enumeration.objects.get(id=enumeration_id)
            e.licenses.add(l)
            e.save()
            messages.success(request, "Your license was automatically verified.")
            return HttpResponseRedirect(reverse('edit_enumeration',
                                args=(enumeration_id,)))
            
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('auto-license-verify.html',
                                            {'form': form,
                                             'name':name,
                                             'enumeration_id': enumeration_id},
                                            RequestContext(request))
            
    #this is a GET
    context= { 'name':name, 'form': AutoVerifyLicenseForm(),
              'enumeration_id': enumeration_id}
    return render_to_response('auto-license-verify.html',
                              RequestContext(request, context,))
