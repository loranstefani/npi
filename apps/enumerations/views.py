from django.conf import settings
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
from models import Enumeration
from ..addresses.models import Address
from ..licenses.models import License
from ..taxonomy.models import TaxonomyCode
from ..specialties.models import SpecialtyCode
import sys
from forms import *
from ..addresses.forms import *
from utils import get_enumeration_user_manages_or_404
from ..surrogates.models import Surrogate, SurrogateRequestEnumeration, SurrogateRequestEIN
import reversion
from baluhn import generate


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
    name = _("Create New Entity for Enumeration")
    if request.method == 'POST':

        form = CreateEnumeration2Form(request.POST)

        if form.is_valid():
            e = Enumeration(enumeration_type = form.cleaned_data['enumeration_type'])
            e.save(commit=False)
            e.last_updated_ip=request.META['REMOTE_ADDR']
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
@staff_member_required
@reversion.create_revision()
def reactivate(request, id):
    name = _("Reactivate a Deactivated Enumeration")
    e = get_object_or_404(Enumeration, id=id)
    if e.status != "A":
        e.status = "A"
        e.last_updated_ip=request.META['REMOTE_ADDR']
        e.save()
        reversion.set_user(request.user)
        reversion.set_comment("Reactivated a Deactivated Enumeration.")
        messages.success(request, "This record has been reactivated.")
    else:
        messages.success(request, "This record was already active. Nothing was done.")
    return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))
    



@login_required
@staff_member_required
@reversion.create_revision()
def replace(request, id):
    name = _("Replace an issued Enumeration number with a new number.")
    e = get_object_or_404(Enumeration, id=id)
    
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
    reversion.set_user(request.user)
    rmsg = "Replacement: %s", (msg)
    reversion.set_comment(rmsg)
    messages.success(request, msg)

    return HttpResponseRedirect(reverse('edit_enumeration', args=(id,)))




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
    e = get_enumeration_user_manages_or_404(Enumeration, id, request.user)
    e.managers.remove(e)
    s = Surrogate.objects.get(user=request.user)
    s.enumerations.remove(e)
    msg = _("You are no longer managing.")
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
        form = DomesticAddressForm(request.POST, instance=address)
        if form.is_valid():
            a = form.save(commit=False)
            a.last_updated_ip=request.META['REMOTE_ADDR']
            a.save()
            reversion.set_user(request.user)
            reversion.set_comment("Create/Edit Domestic Address")
            #based on address_purpose,

            return HttpResponseRedirect(reverse('edit_enumeration',
                                    args=(enumeration_id, )))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
             
    #this is a GET
    context= {'name':name, 'form': DomesticAddressForm(instance=address)}
    return render(request, 'generic/bootstrapform.html', context)




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

