from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from ..surrogates.models import Surrogate
from ..enumerations.models import Enumeration
from ..accounts.forms import LoginForm

def home(request):
    if request.user.is_authenticated():
        return authenticated_home(request) 
    else:
       
       context ={'form': LoginForm()}
       return render_to_response('index.html',
                              RequestContext(request, context,)) 


@login_required
def authenticated_home(request):
    try:
        s = Surrogate.objects.get(user=request.user)
    except Surrogate.DoesNotExist:
        s = Surrogate.objects.create(user=request.user)
    
    name = "Authenticated Home"
    #this is a GET
    context= {'name':name,
              'surrogate': s,
              }
    return render_to_response('authenticated-home.html',
                              RequestContext(request, context,))
    
