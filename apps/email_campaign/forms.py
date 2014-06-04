#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import os, uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from utils import valid_dmf


class SNSForm(forms.Form):
    pass
    
    
    