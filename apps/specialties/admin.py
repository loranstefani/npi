from django.contrib import admin
from models import SpecialtyCode



class SpecialtyCodeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'code', 'taxonomy')
    search_fields = ('description', 'taxonomy', 'code', )
admin.site.register(SpecialtyCode, SpecialtyCodeAdmin)
