from django.db import models


class Notification(models.Model):
    headers     = models.TextField(max_length=1024, blank=True, default ="")
    body        = models.TextField(max_length=4096, blank=True, default ="")
    email       = models.EmailField(max_length=150, blank=True, default="")
    notification_type  = models.CharField(max_length=150, blank=True, default="")
    valid_json  = models.BooleanField(default=False, blank=True)
    added       = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    
    def __unicode__(self):
        return "%s -%s" % (self.id, self.email)