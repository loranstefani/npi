from django.contrib import admin
from models import Specialty



class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'code', 'taxonomy')
    search_fields = ('description', 'taxonomy', 'code', )
admin.site.register(Specialty, SpecialtyAdmin)
