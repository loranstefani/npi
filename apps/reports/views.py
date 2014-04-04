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

@login_required
@staff_member_required
def report_index(request):
    print "erer"
    context ={'foo': 'bar'}
    return render(request,'report-index.html',context)