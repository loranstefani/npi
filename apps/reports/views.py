from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from forms import DateRangeForm, PendingEnumerationForm

@login_required
@staff_member_required
def report_index(request):
    context ={'foo': 'bar'}
    return render(request,'report-index.html',context)
    
@login_required
@staff_member_required
def pending_applications(request):
    name = "Pending Applications"
    if request.method == 'POST':
        form = PendingEnumerationForm(request.POST)
    
        if form.is_valid():
            
            qs = form.save()
            context= {'name':name, 'search_results': qs}
            return render(request, 'pending-applications.html', context)
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'daterange.html', context)
    
    #this is a GET
    context= {'name':name,
              'form': PendingEnumerationForm()}
    return render(request, 'daterange.html', context)
    
    
    
    