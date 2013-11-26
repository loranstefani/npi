import os
import sys
sys.path.append('/home/ubuntu/django-projects/npi')
os.environ['DJANGO_SETTINGS_MODULE'] = 'npi.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
