from django.contrib import admin
from models import Identifier



class IdentifierAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'code', 'state', 'issuer')
    search_fields = ('identifier', 'code', 'state', 'issuer')
admin.site.register(Identifier, IdentifierAdmin)
