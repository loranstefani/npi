from django.db import models
import json

class Notification(models.Model):
    headers     = models.TextField(max_length=1024, blank=True, default ="")
    body        = models.TextField(max_length=4096, blank=True, default ="")
    email       = models.TextField(max_length=300, blank=True, default="")
    notification_type  = models.CharField(max_length=150, blank=True, default="")
    valid_json  = models.BooleanField(default=False, blank=True)
    added       = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    
    def __unicode__(self):
        return "%s -%s" % (self.id, self.email)
        
    
    
    def save(self, **kwargs):
        emails=[]
        
        if self.body:
            try:
                pj = json.loads(str(self.body))

                #load POST SNS response into Model
                if pj.__contains__('Message'):

                    message = json.loads(pj['Message'])                    
                    self.notification_type = message["notificationType"]
                    
                    """If A Bounce """
                    if self.notification_type == "Bounce":  
                        for r in message['bounce']["bouncedRecipients"]:
                                emails.append(r["emailAddress"])
                                
                    """If A Complaint """
                    if self.notification_type == "Complaint":  
                        for r in message['complaint']["complaintRecipients"]:
                                emails.append(r["emailAddress"])
                self.valid_json=True
                self.email = ",".join(emails)
            except ValueError:
                """Doesnt appear to be valid JSON"""
                self.valid_json = False
        super(Notification, self).save(**kwargs)