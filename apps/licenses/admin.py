from django.contrib import admin
from models import License



class LicenseAdmin(admin.ModelAdmin):

    list_display = ('number', 'state', 'license_type', 'status', 'verified')      
    search_fields = ('number', 'state', 'license_type',)

admin.site.register(License, LicenseAdmin)


