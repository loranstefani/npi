from django.contrib import admin
from models import Address, Enumeration, License




#class TaxonomyCodeAdmin(admin.ModelAdmin):
#    list_display = ('npi_worthy', 'code', 'description', 'url')


admin.site.register(Address)
admin.site.register(Enumeration)
admin.site.register(License)
