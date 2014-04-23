from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
import random
from ..enumerations.models import Enumeration


def display_enumeration_profile(request, number):
    
    e = get_object_or_404(Enumeration, number=number, status="A")
    random_background = "%s.jpg" % (random.randrange(1,27))
    context ={"enumeration": e,
              "random_bg_image": random_background,
              }    
    return render(request,'stylish-portfolio.html', context) 

@login_required
@staff_member_required
def display_enumeration_profile_by_id(request, enumeration_id):
    
    e = get_object_or_404(Enumeration, id = enumeration_id)
    random_background = "%s.jpg" % (random.randrange(1,27))
    context ={"enumeration": e,
              "random_bg_image": random_background,
              }
    return render(request,'stylish-portfolio.html', context) 


def display_enumeration_profile_handle(request, handle):
    e = get_object_or_404(Enumeration, handle=handle)
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