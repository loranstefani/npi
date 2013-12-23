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


from forms import SearchForm



#@login_required
def search(request):
    name = _("Search for Providers")
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            a = form.save()
            return render_to_response('search-results.html',
                                            {'form': form,'name':name,},
                                            RequestContext(request))
            
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,'name':name,},
                                            RequestContext(request))
            
    #this is a GET
    context= {'name':name,
              'form': SearchForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))
