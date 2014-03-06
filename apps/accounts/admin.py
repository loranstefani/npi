from django.contrib import admin
from models import ValidPasswordResetKey, Invitation



admin.site.register(ValidPasswordResetKey)

class InvitationAdmin(admin.ModelAdmin):
    
    list_display =  ('email', 'code', 'valid')
    search_fields = ('code', 'valid', 'email')
    
admin.site.register(Invitation, InvitationAdmin)