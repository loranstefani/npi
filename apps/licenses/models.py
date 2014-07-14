from django.db import models
from localflavor.us.us_states import US_STATES
from django.conf import settings

LICENSE_STATUS_CHOICES =( ("", "Unknown"),
                          ("ACTIVE","Active"),
                          ("ACTIVE_WITH_RESTRICTIONS","Active with Restrictions"),
                          ("EXPIRED","Expired"),
                          ("REVOKED","Revoked"),
                          ("DECEASED","Deceased"), )


class LicenseType(models.Model):
    state          = models.CharField(max_length=2,
                                    choices = US_STATES)
    license_type   = models.CharField(max_length=3)
    
    mac            =  models.IntegerField(max_length=2,
                        verbose_name = "Medicare Administrative Contractor")
    
    provider_type  = models.IntegerField(max_length=2)
    
    credential     = models.CharField(max_length=150)
    last_updated_ip     = models.GenericIPAddressField(max_length=20, null=True,
                                default="", db_index=True)
    
    class Meta:
        
        unique_together =  (('state', 'license_type'), )
        ordering = ('state', 'license_type')

    def __unicode__(self):
        lt ="%s-%s (%s)" % (self.state, self.license_type, self.credential)
        return lt
    
    def code(self):
        lt ="%s-%s" % (self.state, self.license_type)
        return lt



class License(models.Model):
    
    license_type   = models.ForeignKey(LicenseType)
    number         = models.CharField(max_length=20, verbose_name="License Number",
                                                    db_index=True)
    status         = models.CharField(max_length=10, choices=LICENSE_STATUS_CHOICES,
                                         default ="")
    verified_by_issuing_board   = models.BooleanField(default=False)
    verified_by_ther_means      = models.BooleanField(default=False)
    verified                    = models.BooleanField(default=False, editable=False)
    note                        = models.TextField(max_length=255,
                                                   blank=True, default="")
    internal_note               = models.TextField(max_length=255,
                                                   blank=True, default="")
    note_restictions            = models.TextField(max_length=1024,
                                                   blank=True, default="")
    license_image               = models.ImageField(blank = True,
                                    null=False, default="",
                                    max_length=255L, upload_to="licenses-",
                                    verbose_name= "License Image",
                                    help_text= "PNG, JPG, or PDF formats accepted. 3MB max.")
    added                       = models.DateField(auto_now_add=True)
    updated                     = models.DateField(auto_now=True)
    last_updated_ip             = models.CharField(max_length=20, blank=True,
                                                    default="", db_index=True)
    
    
    def save(self, **kwargs):
        if self.verified_by_issuing_board or self.verified_by_ther_means:
            self.verified=True
        else:
            self.verified=False        
        super(License, self).save(**kwargs)
    
    
    def __unicode__(self):
        r ="%s-%s" % (self.license_type.code(), self.number)
        return r

    def mlvs(self):
        r ="%s-%s" % (self.license_type.code(), self.number)
        return r

    class Meta:
        
        unique_together =  (('license_type', 'number'), )   

class LicenseValidator(models.Model):

    license_type  = models.ForeignKey(LicenseType)
    # the url will get following appended.
    # /license/[state]/[License_type]/[number].json
    url   = models.CharField(max_length=200, default ="")
    
    def __unicode__(self):
        return str(self.license_type)
   