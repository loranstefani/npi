from django.contrib import admin
from models import TaxonomyCode


class TaxonomyCodeAdmin(admin.ModelAdmin):
    list_display = ( 'code', 'npi_worthy', 'description', 'taxclass','url')
    search_fields = ('code', 'description', 'taxclass')


admin.site.register(TaxonomyCode, TaxonomyCodeAdmin)
