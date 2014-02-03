from django.contrib import admin
from models import Enumeration



class EnumerationAdmin(admin.ModelAdmin):
    list_display = ('name', 'enumeration_type', 'number', 'status', )
    search_fields = ('number', 'status', 'first_name', 'last_name',
              'organization_name')
admin.site.register(Enumeration, EnumerationAdmin)



