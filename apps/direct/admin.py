from django.contrib import admin
from models import DirectAddress, DirectCertificate



class DirectAddressAdmin(admin.ModelAdmin):

    list_display = ('email', 'dns', 'status', 'verified', 'updated')      
    search_fields = ('email', 'dns',)

admin.site.register(DirectAddress, DirectAddressAdmin)

class DirectCertificateAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'dns', 'updated')      
    search_fields = ('dns', 'updated',)

admin.site.register(DirectCertificate, DirectCertificateAdmin)
