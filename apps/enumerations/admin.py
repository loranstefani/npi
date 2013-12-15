from django.contrib import admin
from models import Address, Enumeration, License



class EnumerationAdmin(admin.ModelAdmin):
    list_display = ('enumeration_type', 'number', 'status', 'name')
    search_fields = ('number', 'status', 'first_name', 'last_name',
              'organization_name')
admin.site.register(Enumeration, EnumerationAdmin)




#class TaxonomyCodeAdmin(admin.ModelAdmin):
#    list_display = ('npi_worthy', 'code', 'description', 'url')


admin.site.register(Address)
#admin.site.register(Enumeration)
admin.site.register(License)
