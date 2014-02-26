from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import random
from django.utils.translation import ugettext_lazy as _

from ..enumerations.models import Enumeration

def display_enumeration_profile(request, number):
    
    e = get_object_or_404(Enumeration, number=number, status="A")
    random_background = "%s.jpg" % (random.randrange(1,27))
    context ={"enumeration": e,
              "random_bg_image": random_background,
              }
    
    return render(request,'stylish-portfolio.html', context) 


def display_random_enumeration_profile(request):
    
    id = random.randrange(1,300000)
    e = get_object_or_404(Enumeration, pk=id, status="A")
    random_background = "%s.jpg" % (random.randrange(1,27))
    context ={"enumeration": e,
              "random_bg_image": random_background,
              }
    return render(request,'stylish-portfolio.html', context) 