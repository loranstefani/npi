from django.contrib import admin
from models import License, LicenseValidator



class LicenseAdmin(admin.ModelAdmin):

    list_display = ('number', 'state', 'license_type', 'status', 'verified')      
    search_fields = ('number', 'state', 'license_type',)

admin.site.register(License, LicenseAdmin)


class LicenseValidatorAdmin(admin.ModelAdmin):

    list_display = ('state', 'url')      
    search_fields = ('state', 'url',)

admin.site.register(LicenseValidator, LicenseValidatorAdmin)
