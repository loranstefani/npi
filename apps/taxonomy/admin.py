from django.contrib import admin
from models import TaxonomyCode


class TaxonomyCodeAdmin(admin.ModelAdmin):
    list_display = ('npi_worthy', 'code', 'description', 'url')


admin.site.register(TaxonomyCode, TaxonomyCodeAdmin)
