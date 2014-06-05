from django.contrib import admin
from models import Notification



class NotificationAdmin(admin.ModelAdmin):

    list_display = ('id', 'email', 'notification_type', 'added', 'updated')      
    search_fields = ('email', 'notification_type',)

admin.site.register(Notification, NotificationAdmin)

