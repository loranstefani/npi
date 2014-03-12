from django.contrib import admin
from models import License, LicenseValidator, LicenseType



class LicenseTypeAdmin(admin.ModelAdmin):

    list_display = ('code', 'state', 'license_type', 'credential',  'provider_type', 'mac')      
    search_fields = ('state', 'license_type', 'provider_type', 'mac', 'credential')

admin.site.register(LicenseType, LicenseTypeAdmin)




class LicenseAdmin(admin.ModelAdmin):

    list_display = ('number', 'license_type', 'status', 'verified')      
    search_fields = ('number', 'license_type',)

admin.site.register(License, LicenseAdmin)


class LicenseValidatorAdmin(admin.ModelAdmin):

    list_display = ('license_type', 'url')      
    search_fields = ('license_type', 'url',)

admin.site.register(LicenseValidator, LicenseValidatorAdmin)
