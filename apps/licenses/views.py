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
from ..enumerations.utils import get_enumeration_user_manages_or_404

@login_required
def manual_add_license(request, enumeration_id):
    name = _("Add License")
    if request.method == 'POST':
        form = CreateLicenseForm(request.POST)
        
        if form.is_valid():
            e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
            l = form.save()
            e.licenses.add(l)
            e.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
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
            e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
            l = form.save(commit=False)
            l.verified_by_issuing_board = True
            l.status = "ACTIVE"
            l.save(commit=False)
            l.last_updated_ip=request.META['REMOTE_ADDR']
            l.save()
            
            e.licenses.add(l)
            e.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
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
    
    
@login_required
def delete_license(request, license_id, enumeration_id):
    
    name = _("Delete a License from an Enumeration")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
    l = License.objects.get(id=license_id)       
    e.licenses.remove(l)
    e.save(commit=False)
    e.last_updated_ip=request.META['REMOTE_ADDR']
    e.save()
    l.delete()
    messages.success(request, "Your license was deleted.")
    return HttpResponseRedirect(reverse('edit_enumeration',
                                args=(enumeration_id,)))
