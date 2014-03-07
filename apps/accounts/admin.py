from django.contrib import admin
from models import ValidPasswordResetKey, Invitation, RequestInvite



admin.site.register(ValidPasswordResetKey)

class InvitationAdmin(admin.ModelAdmin):
    
    list_display =  ('email', 'code', 'valid', 'added')
    search_fields = ('code', 'valid', 'email')
    
admin.site.register(Invitation, InvitationAdmin)

class RequestInviteAdmin(admin.ModelAdmin):
    
    list_display =  ('first_name', 'last_name', 'organization', 'email', 'added')
    search_fields = ('first_name', 'last_name', 'organization', 'email')
    
admin.site.register(RequestInvite, RequestInviteAdmin)