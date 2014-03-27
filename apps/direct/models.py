from django.db import models
from localflavor.us.us_states import US_STATES


class DirectAddress(models.Model):
    
    email         = models.EmailField(max_length=150, db_index=True)
    organization  = models.CharField(max_length=150,  default="")
    dns           = models.CharField(max_length=150,  blank=True, default="",
                                    editable=False, db_index=True)
    status      = models.CharField(max_length=10, blank=True,default ="")
    verified    = models.BooleanField(default=False, editable=False)
    added       = models.DateField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    last_updated_ip     = models.GenericIPAddressField(max_length=20, null=True,
                                default="", db_index=True)
    
    def __unicode__(self):
        return self.dns


    def save(self, **kwargs):
        
        self.dns = self.email.replace("@", ".")     
        super(DirectAddress, self).save(**kwargs)
        
        
        
class DirectCertificate(models.Model):
    

    dns         = models.CharField(max_length=3000,  blank=True, default="",
                                    #editable=False,
                                    db_index=True)
    file        = models.FileField(blank = True, null=False, default='',
                        max_length=255L, upload_to="direct_pems",
                        verbose_name= "Direct Public Certificate",
                        help_text ="This is an x509 Public Certificate in PEM format.")
    added       = models.DateField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    last_updated_ip     = models.GenericIPAddressField(max_length=20, null=True,
                                default="", db_index=True)
   

    
    def __unicode__(self):
        return str(self.id)


    def save(self, **kwargs):
         
        super(DirectCertificate, self).save(**kwargs)