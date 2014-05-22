from django.contrib import admin
from models import DeceasedMasterFile



class DeceasedMasterFileAdmin(admin.ModelAdmin):

    list_display = ('file', 'processed', 'added', 'updated')      

admin.site.register(DeceasedMasterFile, DeceasedMasterFileAdmin)

