from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from ..enumerations.models import Enumeration
from models import Surrogate, SurrogateRequest
from utils import send_email_to_newly_authorized_manager
# Create your views here.


def grant_management(request, key):
    sr = get_object_or_404(SurrogateRequest,key=key)
    #The key was found so lets gant access
    sr.enumeration.managers.add(sr.user)
    messages.success(request,_("Management authority has been granted to the user."))
    
    #TODO Send a message to I&A that he user has gained a new permission.
    
    
    #Send a message to the requestor that access is now granted.
    send_email_to_newly_authorized_manager(sr)   
    
    
    #cleanup delete the SurrogateRequest object
    sr.delete()
    return HttpResponseRedirect(reverse('home',))
