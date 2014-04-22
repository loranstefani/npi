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
from forms import *
from datetime import timedelta, date, datetime
from ..enumerations.models import Enumeration

@login_required
@staff_member_required
def report_index(request):
    context ={'foo': 'bar'}
    return render(request,'report-index.html',context)



@login_required
@staff_member_required
def pending_application_overview(request):
    name = "Pending Application Overview"
    if request.method == 'POST':
        form = PendingEnumerationOverviewForm(request.POST)
    
        if form.is_valid():
            search_results = form.save()
            context= {'name':           name,
                      'search_results': search_results}
            return render(request, 'pending-overview.html', context)
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = { 'form': form, 'name': name}
             return render(request, 'daterange.html', context)
    
    #this is a GET
    context= {'name':name,
              'form': PendingEnumerationOverviewForm()}
    return render(request, 'daterange.html', context)

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
    
@login_required
@staff_member_required   
def enumerations_stats_by_state(request):
    name = "Enumeration Statistics By State"
    if request.method == 'POST':
        form = EnumerationsStatisByStateForm(request.POST)
    
        if form.is_valid():
            search_results = form.save()
            context= {'name':name, 'search_results': search_results, }
            return render(request, 'enumeration-stats-by-state.html', context)
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'daterange.html', context)
    
    #this is a GET
    context= {'name':name,
              'form': EnumerationsStatisByStateForm()}
    return render(request, 'daterange.html', context)    
    
    
    
@login_required
@staff_member_required   
def enumerated_applications(request):
    name = "Enumerated Applications"
    if request.method == 'POST':
        form = EnumeratedApplicationsForm(request.POST)
    
        if form.is_valid():
            search_results = form.save()            
            context= {'name':name, 
                      'date_start': form.cleaned_data.get("date_start"),
                       'date_stop': form.cleaned_data.get("date_stop") }
            
            context.update(search_results)
            return render(request, 'enumerated-applications.html', context)
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'daterange.html', context)
    
    #this is a GET
    context= {'name':name,
              'form': EnumeratedApplicationsForm()}
    return render(request, 'daterange.html', context)    
    
    
    
@login_required
@staff_member_required   
def staff_member_summary(request, username, date_start, date_stop):
    name = "Staff Member Summary"
    u = User.objects.get(username=username)
    date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
    date_stop = datetime.strptime(date_stop, '%Y-%m-%d').date()
    total_user_enumerations = Enumeration.objects.filter(enumerated_by=u).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
    total_user_activations = Enumeration.objects.filter(status= "A", enumerated_by=u).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
    total_user_rejections = Enumeration.objects.filter(status= "R", enumerated_by=u).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).count()
    
    enumerations = Enumeration.objects.filter(status= "A", enumerated_by=u).exclude(enumeration_date__lt=date_start).exclude(enumeration_date__gt=date_stop).only('enumeration_date', 'added')
    lte_three = 0
    four_to_five = 0
    gt_five = 0
    
    for e in enumerations:
        delta = e.added - e.enumeration_date
        if int(delta.days) <= 3:
            lte_three += 1
        
        if int(delta.days) == 4 or int(delta.days) == 5:
            four_to_five += 1
        
        if int(delta.days) >= 5:
            gt_five += 1
            
    percent_gt_five = (float(gt_five) / float(total_user_enumerations)) * 100.0
    percent_user_rejects = (float(total_user_rejections) / float(total_user_enumerations)) * 100.0

    context = {'name': name, 'staff_user': u,
               'lte_three': lte_three, 'four_to_five': four_to_five,
               'gt_five': gt_five,     'percent_gt_five': percent_gt_five,
               'total_user_enumerations': total_user_enumerations,
               'total_user_activations': total_user_activations,
               'total_user_rejections': total_user_rejections,
               'percent_user_rejects': percent_user_rejects
               }
    
    return render(request, 'staff-member-summary.html', context)
      