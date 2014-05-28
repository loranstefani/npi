from django.conf import settings
from django.http import Http404
from django.utils.safestring import SafeString
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import uuid, random
from models import Enumeration, GateKeeperError, Event
from ..addresses.models import Address
from ..licenses.models import License
from ..taxonomy.models import TaxonomyCode
from ..specialties.models import SpecialtyCode
import sys, json
from forms import *
from ..addresses.forms import *
from utils import get_enumeration_user_manages_or_404
from ..surrogates.models import Surrogate, SurrogateRequestEnumeration, SurrogateRequestEIN
import reversion
from baluhn import generate
from emails import send_pending_email, send_active_email

@login_required
@reversion.create_revision()
def primary_taxonomy(request, enumeration_id):
    name = _("Select a Primary Taxonomy")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id, request.user)

    if request.method == 'POST':
        form = PrimaryTaxonomyForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.status="E"
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Primary taxonomy created/updated.")
            messages.success(request,_("The primary taxonomy was updated/created."))
            return HttpResponseRedirect(reverse('edit_enumeration', args=(enumeration_id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    #this is a GET
    context= {'name':name,
              'form': PrimaryTaxonomyForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)



@login_required
@reversion.create_revision()
def primary_specialty(request, enumeration_id):
    name = _("Select a Primary Specialty")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id, request.user)

    if request.method == 'POST':
        form = PrimarySpecialtyForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            if not e.taxonomy:
                try:
                    print e.specialty.taxonomy
                    t = TaxonomyCode.objects.get(code=e.specialty.taxonomy)
                    
                    print 
                    e.taxonomy = t
                    msg = "Your taxonomy code was set automatcially to %s based on your specialty. You can change it if need be." % (t)
                    messages.info(request,_(msg))
                except TaxonomyCode.DoesNotExist:
                    pass            
            else:
                msg = "Based on your specialty we suggest the Taxonomy code %s" % (e.specialty.taxonomy)
                messages.info(request,_(msg))    
            
            
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Primary specialty created/updated.")
            messages.success(request,_("The primary specialty was updated/created."))
            return HttpResponseRedirect(reverse('edit_enumeration', args=(enumeration_id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    #this is a GET
    context= {'name':name,
              'form': PrimarySpecialtyForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)


@login_required
@reversion.create_revision()
def add_other_taxonomies(request, enumeration_id):
    name = _("Add Other Taxonomies")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)

    if request.method == 'POST':
        form = OtherTaxonomyForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()
            form.save()
            form.save_m2m()
            reversion.set_user(request.user)
            reversion.set_comment("Added/Changed other taxonomies.")
            messages.success(request,_("Other taxonomies were added/changed."))
            return HttpResponseRedirect(reverse('edit_enumeration',
                                                args=(enumeration_id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    #this is a GET
    context= {'name':name,
              'form': OtherTaxonomyForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)


@login_required
@reversion.create_revision()
def delete_other_taxonomy(request, taxonomy_id, enumeration_id):
    name = _("Delete Other Taxonomies")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)

    t = TaxonomyCode.objects.get(id=taxonomy_id)
    e.other_taxonomies.remove(t)
    e.save(commit=False)
    e.last_updated_ip=request.META['REMOTE_ADDR']
    e.save()
    reversion.set_user(request.user)
    reversion.set_comment("Other taxonomy deleted.")
    messages.success(request,_("The other taxonomy was deleted."))
    return HttpResponseRedirect(reverse('edit_enumeration', args=(enumeration_id,)))


def search_enumeration(request):
    name = _("Search")
    if request.method == 'POST':

        form = SearchForm(request.POST,)

        if form.is_valid():
            qs = form.save()
            context= {'name':name,
                      'search_results': qs,
              'form': SearchForm()}
            return render(request, 'search.html', context)

        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)

    #this is a GET
    context= {'name':name,
              'form': SearchForm()}
    return render(request, 'generic/bootstrapform.html', context)



@login_required
def surrogate_lookup(request):
    name = _("Search for an Enumeration to Manage")
    if request.method == 'POST':

        form = SearchForm(request.POST,)

        if form.is_valid():
            qs = form.save()
            context= {'name':name,
                      'search_results': qs,
              'form': SearchForm()}
            return render_to_response('surrogate-search.html',
                              RequestContext(request, context,))

        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)

    #this is a GET
    context= {'name':name,
              'form': SearchForm()}
    return render(request, 'generic/bootstrapform.html', context)




@login_required
def ein_lookup(request):
    name = _("Search for an EIN to Manage")
    if request.method == 'POST':

        form = SearchEINForm(request.POST,)

        if form.is_valid():
            qs = form.save()
            context= {'name':name,
                      'search_results': qs,
                      'ein':form.cleaned_data.get("ein", "")}
            return render_to_response('ein-search.html',
                              RequestContext(request, context,))

        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)

    #this is a GET
    context= {'name':name,
              'form': SearchEINForm()}
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))




@login_required
def request_to_manage_enumeration(request, id):
    e = get_object_or_404(Enumeration, id=id)

    #Send an email to the authorized contact by creating a Surrogate Request
    sr = SurrogateRequestEnumeration.objects.create(user=request.user, enumeration=e)
    #Add the enumeration to request.user's surrogate list
    s = Surrogate.objects.get(user=request.user)
    s.enumerations.add(e)
    s.save()
    msg = _("Your request to manage the enumeration was sent to the authorized official")
    messages.success(request, msg)
    return HttpResponseRedirect(reverse('home'))


@login_required
def request_to_manage_ein(request, ein):
    enumerations = Enumeration.objects.filter(ein=ein)
    sr = SurrogateRequestEIN.objects.create(user=request.user, ein=ein)

    for e in enumerations:
        #Add the enumeration to request.user's surrogate list
        s = Surrogate.objects.get(user=request.user)
        s.enumerations.add(e)
        s.save()

    msg = _("Your request to manage EIN was sent to the authorized officials")
    messages.success(request, msg)
    return HttpResponseRedirect(reverse('home'))


@login_required
@reversion.create_revision()
def create_enumeration(request):
    name = _("Create a New Provider Identifier")
    if request.method == 'POST':

        form = CreateEnumeration2Form(request.POST)

        if form.is_valid():
            e = Enumeration(enumeration_type = form.cleaned_data['enumeration_type'])
            e.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.status="E"
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Created Enumeration.")
            
            e.managers.add(request.user)
            

            #make sure this user is also the surrogate

            s = Surrogate.objects.get(user=request.user)
            s.save()
            s.enumerations.add(e)
            s.save()

            if e.enumeration_type in ("NPI-1", "OEID-1"):
               return HttpResponseRedirect(reverse('create_individual_enumeration',
                                                   args=(e.id,)))
            else:
                return HttpResponseRedirect(reverse('create_organization_enumeration',
                                                   args=(e.id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)

    #this is a GET
    context= {'name':name,
              'form': CreateEnumeration2Form()}
    return render(request, 'generic/bootstrapform.html', context)



@login_required
def edit_basic_enumeration(request, id):
    name = _("Edit basic information for an enumeration")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    if e.enumeration_type in ("NPI-1", "OEID-1"):
        return HttpResponseRedirect(reverse('edit_individual_enumeration',
                                                   args=(e.id,)))
    else:
        return HttpResponseRedirect(reverse('edit_organization_enumeration',
                                                   args=(e.id,)))


@login_required
@reversion.create_revision()
def self_take_over(request):
    
    name = "Take control of your individual provider identifer"
    if request.method == 'POST':
        form = SelfTakeOverForm(request.POST)
        if form.is_valid():
            e = form.get_enumeration()
            #Give ownership to the individual
            
            e.managers.add(request.user)
            #make sure this user is also the surrogate
            s = Surrogate.objects.get(user=request.user)
            s.save()
            s.enumerations.add(e)
            s.save()
            reversion.set_user(request.user)
            reversion.set_comment("Self Take Over")
            messages.success(request,_("You are now in control of your own record."))
            return HttpResponseRedirect(reverse('edit_enumeration', args=(e.id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    
    
    
    
    #this is a GET
    context= {'name':name,
              'form': SelfTakeOverForm()}
    return render(request, 'generic/bootstrapform.html', context)
    
    


@login_required
@reversion.create_revision()
def edit_pii(request, id):
    name = _("Birtday, SSN, and ITIN")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    
    #Do not let this function work if the PII is already locked.
    if e.pii_lock:
        raise Http404()
    
    if request.method == 'POST':
        form = IndividualPIIForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.status="E"
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Edit personal PII.")
            return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
             
    #this is a GET
    context= {'name':name,
              'form': IndividualPIIForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)




@login_required
@reversion.create_revision()
def contact_person(request, id):
    name = _("Contact Person")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    if request.method == 'POST':
        form = ContactPersonForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Edit Contact Person.")
            return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
             
    #this is a GET
    context= {'name':name,
              'form': ContactPersonForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)

@login_required
@reversion.create_revision()
def authorized_official(request, id):
    name = _("Authorized Official")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    if request.method == 'POST':
        form = AuthorizedOfficialForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Edit Authorized Official.")
            return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
             
    #this is a GET
    context= {'name':name,
              'form': AuthorizedOfficialForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)


@login_required
@reversion.create_revision()
def other_names(request, id):
    name = _("Other Names")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    if request.method == 'POST':
        form = OtherNamesForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Edit Other Names.")

            return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    #this is a GET
    context= {'name':name,
              'form': OtherNamesForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)

@login_required
@reversion.create_revision()
def create_individual_enumeration(request, id):
    name = _("Create a New Individual")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)


    if request.method == 'POST':
        form = CreateEnumerationIndividualForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save()
            reversion.set_user(request.user)
            reversion.set_comment("Create Individual Enumeration.")
            return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    #this is a GET
    context= {'name':name,
              'form': CreateEnumerationIndividualForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)



@login_required
@reversion.create_revision()
def create_organization_enumeration(request, id):
    name = _("Create a New Organization")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)


    if request.method == 'POST':
        form = CreateEnumerationOrganizationForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Create/Edit Organization Enumeration.")
            return HttpResponseRedirect(reverse('edit_enumeration',
                                                   args=(e.id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    #this is a GET
    context= {'name':name,
              'form': CreateEnumerationOrganizationForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)



@login_required
@reversion.create_revision()
def flag_for_fraud(request, id):
    name = _("Flag for Fraud")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    if request.method == 'POST':
        form = FraudAlertForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Flag for Fraud.")
            messages.success(request, "This record has been flagged for fraud.")
            return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,'name':name,},
                                            RequestContext(request))
    #this is a GET
    context= {'name':name,
              'form': FraudAlertForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)


@login_required
@reversion.create_revision()
def flag_for_deactivation(request, id):
    name = _("Flag for Deactivation")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    if request.method == 'POST':
        form = DeactivateEnumerationForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Flag for Deactivation.")
            messages.success(request, "This record has been flagged for deactivation.")
            return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
             
    #this is a GET
    context= {'name':name,
              'form': DeactivateEnumerationForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)




@login_required
@reversion.create_revision()
def submit_dialouge(request, id):
    name = _("Submit Application for Enumeration")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    
    if e.status == "A":
        messages.info(request, "This enumertation is already active and does not require re-submission.")
        return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
     
    if request.method == 'POST':
        form = SubmitApplicationForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            errors = e.gatekeeper()
            if not errors:
                e.status="A"
                e.enueration_date = datetime.date.today()
                e.last_update     = datetime.date.today()
                system_user       = User.objects.get(username=settings.AUTO_ENUMERATION_USERNAME)
                e.enumerated_by= system_user
                e.save()
                send_active_email(e)
                msg = "The application has been automaticaly enumerated. The number issued is %s." % (e.number)
                messages.success(request, msg)
                reversion.set_comment("Submit Enumeration Application - Auto-Enumerated")
                Event.objects.create(enumeration=e, event_type="ACTIVATION",
                             note= msg)
                
            else:
                for i in errors:
                    if i.critical_error:
                        msg = "The application cotains critical errors and cannot be submitted." 
                        messages.error(request, msg)
                        return HttpResponseRedirect(reverse('edit_enumeration',
                                                   args=(e.id,)))
                
                #No xcritical errors so we let it pend for the enumerator to figure it out.
                e.status="P"
                e.save()
                send_pending_email(e)
                messages.info(request, "This application has been received and is pending.")
                reversion.set_comment("Submit Enumeration Application - Pending")

            reversion.set_user(request.user)
            return HttpResponseRedirect(reverse('home'))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
             
    #this is a GET
    errors = e.gatekeeper()
    critical_errors = False
    for i in errors:
        if i.critical_error:
            critical_errors = True        
            msg = "%s (Critical)" % (i.note)
        else:
            msg = i.note        
        messages.error(request, msg)
    if critical_errors:
        msg = """The application contains one or more critical errors that are preventing the application submission.
        Fix these errors, then resubmit you application for enumeration.
        """
        messages.error(request, msg)
        return HttpResponseRedirect(reverse('edit_enumeration',
                                                   args=(e.id,)))

        
    if not errors:
        messages.success(request, "Congratulations. No validation errors were detectd with this application.")
    else:
        msg = """You can <a href="%s">go back attempt to fix these errors</a>
        or continue to submit your application with errors. The enumeration process may be
        stalled or delayed when errors are present.""" % (reverse('edit_enumeration', args=(id,)))
        messages.info(request, SafeString(msg))

    
    context= {'name':name,
              'form': SubmitApplicationForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)


@login_required
@staff_member_required
@reversion.create_revision()
def reactivate(request, id):
    name = _("Reactivate a Deactivated Enumeration")
    e = get_object_or_404(Enumeration, id=id)
    if e.status == "D":
        
        
        #Remove all gatekeeper errors.
        GateKeeperError.objects.filter(enumeration=e).delete()
        
        # Status A
        e.status = "A"
        e.last_updated_ip=request.META['REMOTE_ADDR']
        e.enumerated_by = request.user
        e.save()
        msg = "This record has been reactivated by %s" % (request.user)
        Event.objects.create(enumeration=e, event_type="REACTIVATION",
                             note= msg)
        reversion.set_user(request.user)
        reversion.set_comment(msg)
        messages.success(request, msg)
    elif e.status == "A":
        messages.info(request, "This record was not deactivated. Nothing was done.")
    else:
        messages.info(request, "This record was not deactivated. Nothing was done.")
    return HttpResponseRedirect(reverse('report_index'))
    


@login_required
@staff_member_required
@reversion.create_revision()
def activate(request, id):
    name = _("Activate an Enumeration")
    e = get_object_or_404(Enumeration, id=id)

    if e.has_ever_been_active:
        messages.info(request, "This record has already been activated at least once. Use reactivate to reactivate.")
        
    else:
        if e.status in  ("E", "P"):
            #Remove all gatekeeper errors.
            GateKeeperError.objects.filter(enumeration=e).delete()
            
            
            e.status = "A"
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.enumerated_by = request.user
            e.save()
            msg = "This record has been manually activated by %s." % (request.user)
            Event.objects.create(enumeration=e, event_type="ACTIVATION",
                                 note= msg)
            reversion.set_user(request.user)
            comment = "Enumerated Application. Number is %s" % (e.number)
            reversion.set_comment(comment)
            messages.success(request, msg)
        elif e.status== "A":
            messages.info(request, "This record is already active. Nothing done.")
        
        elif e.status== "D":
            messages.info(request, "This record is deactived. Use reactivate to make it active again.")
        
        elif e.status== "R":
            messages.info(request, "This record was rejected. Activation is not possible.")
        
        
    return HttpResponseRedirect(reverse('report_index'))




@login_required
@staff_member_required
@reversion.create_revision()
def reject(request, id):
    name = _("Activate an Enumeration")
    e = get_object_or_404(Enumeration, id=id)
    if e.status == "P":
        
        
        #Remove all gatekeeper errors.
        GateKeeperError.objects.filter(enumeration=e).delete()
        
        e.status = "R"
        e.last_updated_ip=request.META['REMOTE_ADDR']
        e.enumerated_by = request.user
        e.save()
        msg = "This record has been rejected by %s" % (request.user)
        Event.objects.create(enumeration=e, event_type="REJECTION", note= msg)
        reversion.set_user(request.user)
        comment = "Application. Rejected"
        reversion.set_comment(comment)
        messages.success(request, "This record has been successfully been rejected.")
    else:
        messages.info(request, "This record was not pending so nothing was done. The record was not rejected.")
    return HttpResponseRedirect(reverse('report_index'))



@login_required
@staff_member_required
@reversion.create_revision()
def deactivate(request, id):
    name = _("Deactivate")
    e = get_object_or_404(Enumeration, id=id)
    
    #If status is already deactivated then redirect.
    if e.status == "D":
        messages.info(request, "This record was not deactive so nothing was done. The record was not rejected.")
        return HttpResponseRedirect(reverse('report_index'))
    
    if request.method == 'POST':
        form = DeactivationForm(request.POST, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.status="D"
            e.deactivation_date = datetime.date.today()
            e.save()
            msg = "Enumeration %s has been deactivated by %s." % (e.number, request.user)
            Event.objects.create(enumeration=e, event_type="DEACTIVATION", note= msg)
            reversion.set_user(request.user)
            comment = "Deactivation of %s" % (e.number)
            reversion.set_comment(comment)
            messages.success(request, msg)
            return HttpResponseRedirect(reverse('report_index'))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    #this is a GET
    context= {'name':name,
              'form': DeactivationForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)
    
    
    
@login_required
@staff_member_required
@reversion.create_revision()
def replace(request, id):
    name = _("Replace an issued Enumeration number with a new number.")
    e = get_object_or_404(Enumeration, id=id)
    if e.has_ever_been_active:
        #create a candidate eumeration
        eight_digits = random.randrange(10000000,19999999)                
        prefixed_eight_digits = "%s%s" % (settings.LUHN_PREFIX, eight_digits)
        checkdigit = generate(prefixed_eight_digits)            
        new_number = "%s%s" % (eight_digits, checkdigit)
        while Enumeration.objects.filter(number=new_number).count()>0:
            eight_digits          = random.randrange(10000000,19999999)
            prefixed_eight_digits = "%s%s" % (settings.LUHN_PREFIX, eight_digits)
            checkdigit            = generate(prefixed_eight_digits)
            new_number            = "%s%s" % (eight_digits, checkdigit)
        
        #create a message
        msg = "The number %s has been replaced with %s" % (e.number, new_number)
        
        #Append the old number to the old_numbers field.
        e.old_numbers = "%s, %s" % (e.old_numbers, e.number)
        
        #Remove any command or whitespace from the begining
        if e.old_numbers.startswith(","):
            e.old_numbers = e.old_numbers[1:]
            
        if e.old_numbers.startswith(" "):
            e.old_numbers = e.old_numbers[1:]
        
        #Set the new number
        e.number = new_number
        #flag this recors as having been replaced
        e.is_number_replaced = True
        
        e.last_updated_ip=request.META['REMOTE_ADDR']
        e.save()
        msg = "A new enumeration number %s was assigned." % (e.number)
        
        #Create an event
        Event.objects.create(enumeration=e, event_type="REENUMERATION", note= msg)
        
        reversion.set_user(request.user)
        rmsg = "Replacement: %s", (msg)
        reversion.set_comment(rmsg)
        messages.success(request, msg)
    else:
        messages.info(request, "This record has never been active so a replacement is not allowed.")

    return HttpResponseRedirect(reverse('report_index'))




@login_required
def edit_enumeration(request, id):
    #This is a GET
    name = _("Edit Enumeration")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    context= {'name': name,
              'enumeration': e,
              }
    return render(request, 'edit.html', context)


@login_required
@reversion.create_revision()
def edit_enhanced_enumeration(request, id):
    name = _("Edit Enhanced Profile Information")
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)


    if request.method == 'POST':
        form = EnumerationEnhancementForm(request.POST, request.FILES, instance=e)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.status="E"
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Edit Enhancements.")
            
            
            return HttpResponseRedirect(reverse('edit_enumeration',
                                                   args=(e.id,)))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    #this is a GET
    context= {'name':name,
              'form': EnumerationEnhancementForm(instance=e)}
    return render(request, 'generic/bootstrapform.html', context)

@login_required
def stop_managing_enumeration(request, enumeration_id):
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id, request.user)
    e.managers.remove(e)
    s = Surrogate.objects.get(user=request.user)
    s.enumerations.remove(e)
    msg = "You are no longer managing %s." % (e.name())
    messages.error(request,msg)
    return HttpResponseRedirect(reverse('home',))



@login_required
@reversion.create_revision()
def select_address_type(request, address_purpose, enumeration_id):
    name = _("Create Address")
    if request.method == 'POST':
        form = SelectAddressPurposeForm(request.POST,
                                        address_purpose=address_purpose)
        if form.is_valid():
            a = form.save()

            #save this address to the enumeration.
            e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                                    request.user)


            if str(address_purpose) == "LOCATION":
                e.location_address = a

            if str(address_purpose) == "MAILING":
                e.mailing_address = a

            if str(address_purpose) == "MEDREC-STORAGE":
                e.medical_record_storage_address = a

            if str(address_purpose) == "1099":
                e.ten_ninety_nine_address = a

            if str(address_purpose) == "REVALIDATION":
                e.revalidation_address = a


            if str(address_purpose) in ("OTHER", "ADDITIONAL-LOCATION",):
                e.other_addresses.add(a)

            e.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
            e.save()


            if a.address_type == "DOM":
                return HttpResponseRedirect(reverse('domestic_address',
                                                    args=(a.id, e.id)))
            elif a.address_type == "FGN":
                return HttpResponseRedirect(reverse('foreign_address',
                                                    args=(a.id,e.id, )))
            elif a.address_type == "MIL":
                return HttpResponseRedirect(reverse('military_address',
                                                    args=(a.id,e.id, )))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
             

    #this is a GET
    context= {'name':name,
              'form': SelectAddressPurposeForm(address_purpose=address_purpose)}
    return render(request, 'generic/bootstrapform.html', context)



@login_required
def edit_address(request, address_id, enumeration_id):
    a = Address.objects.get(id=address_id)
    name = _("Edit Address")

    if a.address_type == "DOM":
        return HttpResponseRedirect(reverse('domestic_address',
                                            args=(a.id,enumeration_id)))
    elif a.address_type == "FGN":
        return HttpResponseRedirect(reverse('foreign_address',
                                            args=(a.id,enumeration_id)))
    elif a.address_type == "MIL":
        return HttpResponseRedirect(reverse('military_address',
                                            args=(a.id,enumeration_id)))


    context= {'name':name,
              'form': SelectAddressTypeForm(instance=a)}
    return render(request, 'generic/bootstrapform.html', context)




@login_required
@reversion.create_revision()
def domestic_address(request,  address_id, enumeration_id):
    name = _("Domestic Address")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        form = DomesticAddress2Form(request.POST, instance=address)

        if form.is_valid():
            
            #Get the fields and ensure they validate.
            a               = form.save(commit=False)
            a.city          =  form.cleaned_data.get("city", "")
            a.address_1     =  form.cleaned_data.get("address_1", "")
            a.address_2     =  form.cleaned_data.get("address_2", "")
            a.state         =  form.cleaned_data.get("state", "")
            a.zip           =  form.cleaned_data.get("zip", "")
            
            #hit the smartystreets api
            verify          = a.verify()
            
            if type({}) == type(verify):
                print "Connectivity or auth error"
                #Accept addesss anyway  - Verificain is turned off.
                a = form.save(commit=False)
                a.last_updated_ip=request.META['REMOTE_ADDR']
                a.save()
                reversion.set_user(request.user)
                reversion.set_comment("Create/Edit Domestic Address")
                e.status="E"
                e.save()
            
            else:
                #we got a response from the address service.
                

                print json.dumps(verify, indent=4)
                a = form.save(commit=False)
                a.last_updated_ip=request.META['REMOTE_ADDR']
                a.save()
                reversion.set_user(request.user)
                reversion.set_comment("Create/Edit Domestic Address")
                e.status="E"
                e.save()
                
            
            return HttpResponseRedirect(reverse('edit_enumeration',
                                    args=(enumeration_id, )))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'live-address.html', context)
             
    #this is a GET
    context= {'name':name, 'form': DomesticAddress2Form(instance=address),
              'SMARTY_STREETS_HTML_SECRET': settings.SMARTY_STREETS_HTML_SECRET
              }
    return render(request, 'live-address.html', context)




@login_required
@reversion.create_revision()
def foreign_address(request, address_id, enumeration_id):
    name = _("Foreign Address")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        form = ForeignAddressForm(request.POST, instance=address)
        if form.is_valid():
            a = form.save(commit=False)
            a.last_updated_ip=request.META['REMOTE_ADDR']
            a.save()
            e.status="E"
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Create/Edit Foreign Address")
            return HttpResponseRedirect(reverse('edit_enumeration',
                                    args=(enumeration_id, )))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)

    #this is a GET
    context= {'name':name,
              'form': ForeignAddressForm(instance=address)}
    return render(request, 'generic/bootstrapform.html', context)


@login_required
@reversion.create_revision()
def military_address(request, address_id, enumeration_id):
    name = _("Military Address")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        form = MilitaryAddressForm(request.POST, instance=address)
        if form.is_valid():
            a = form.save(commit=False)
            a.last_updated_ip=request.META['REMOTE_ADDR']
            a.save()
            e.status="E"
            e.save()
            reversion.set_user(request.user)
            reversion.set_comment("Create/Edit Military Address")
            return HttpResponseRedirect(reverse('edit_enumeration',
                                    args=(enumeration_id, )))

        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)

    #this is a GET
    context= {'name':name,
              'form': MilitaryAddressForm(instance=address)}
    return render(request, 'generic/bootstrapform.html', context)


@login_required
@reversion.create_revision()
def delete_address(request,  address_id, enumeration_id):
    name = _("Delete Address")
    e = get_enumeration_user_manages_or_404(Enumeration, enumeration_id,
                                            request.user)
    address = get_object_or_404(Address, id=address_id)
    #address.delete()

    messages.success(request,_("Address deleted."))
    return HttpResponseRedirect(reverse('edit_enumeration',
                                    args=(enumeration_id, )))

