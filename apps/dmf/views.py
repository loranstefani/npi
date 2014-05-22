from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from forms import DMFForm
from models import DeceasedMasterFile
from utils import process_dmf
import os
# Create your views here.


@login_required
@staff_member_required
def dmf_upload(request):
    name = _("DMF Upload")
    if request.method == 'POST':
        form = DMFForm(request.POST, request.FILES)
    
        if form.is_valid():
            # process the dmf.
            
            m =form.save()
            
            total = process_dmf(m.file)            
            full_path = os.path.join(settings.MEDIA_ROOT, str(m.file))
            msg = _("%s matching records were found and flagged as deceased.") % (total)
            messages.success(request, msg)
            m.processed = True
            m.save()
            # Ensure the actual processed DMF file is hidden from the world
            os.chmod(full_path, 0000)
            return HttpResponseRedirect(reverse('report_index'))
            
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             context = {'form': form,'name':name,}
             return render(request, 'generic/bootstrapform.html', context)
    
    #this is a GET
    context= {'name':name,
              'form': DMFForm()}
    return render(request, 'generic/bootstrapform.html', context)
    
