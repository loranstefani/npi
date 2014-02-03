from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.utils.translation import ugettext_lazy as _

from ..enumerations.models import Enumeration

def display_enumeration_profile(request, number):
    e = get_object_or_404(Enumeration, number=number)
    context ={"enumeration": e}
    return render(request,'stylish-portfolio.html', context) 


