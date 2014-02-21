from django.contrib import admin
from models import Address



class AddressAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'address_type', 'address_purpose')
    search_fields = ('address_type', 'address_purpose', 'state', 'country', 'city')
admin.site.register(Address, AddressAdmin)
