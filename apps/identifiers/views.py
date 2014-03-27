from django.shortcuts import render
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
from models import Identifier
from ..enumerations.models import Enumeration
from ..enumerations.utils import get_enumeration_user_manages_or_404
# Create your views here.

@login_required
def add_identifier(request, enumeration_id):
    name = _("Add Identifier")
    if request.method == 'POST':
        form = IdentifierForm(request.POST)
        
        if form.is_valid():
            e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
            i = form.save(commit=False)
            i.last_updated_ip=request.META['REMOTE_ADDR']
            i.save()
            e.identifiers.add(i)
            e.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()
            messages.success(request,_("An Identifier was added to the enumeration."))
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
              'form': IdentifierForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))


@login_required
def delete_identifier(request, identifier_id, enumeration_id):
    
    name = _("Delete an Identifier from an Enumeration")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
    i = Identifier.objects.get(id=identifier_id)       
    e.identifiers.remove(i)
    e.save()
    i.delete()
    messages.success(request, "Your Identifier was deleted from this enumeration.")
    return HttpResponseRedirect(reverse('edit_enumeration',
                                args=(enumeration_id,)))