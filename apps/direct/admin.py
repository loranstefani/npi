from django.contrib import admin
from models import DirectAddress



class DirectAddressAdmin(admin.ModelAdmin):

    list_display = ('email', 'dns', 'status', 'verified',)      
    search_fields = ('email', 'dns',)

admin.site.register(DirectAddress, DirectAddressAdmin)

