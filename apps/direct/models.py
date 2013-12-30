from django.db import models
from localflavor.us.us_states import US_STATES


class DirectAddress(models.Model):
    email         = models.EmailField(max_length=150)
    dns           = models.CharField(max_length=150,  blank=True, default="",
                                    editable=False)
    certificate    = models.FileField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="direct_pems",
                                    verbose_name= "Certificate File")

    status         = models.CharField(max_length=10, blank=True,default ="")
    verified       = models.BooleanField(default=False, editable=False)
   

    
    
    def __unicode__(self):
        return self.dns


    def save(self, **kwargs):
        
        self.dns = self.email.replace("@", ".")     
        super(DirectAddress, self).save(**kwargs)