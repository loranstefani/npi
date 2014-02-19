from django.db import models
from localflavor.us.us_states import US_STATES





LICENSE_STATUS_CHOICES =(("UNKNOWN", "Unknown"),
                          ("ACTIVE","Active"),
                          ("ACTIVE_WITH_RESTRICTIONS","Active with Restrictions"),
                          ("EXPIRED","Expired"),
                          ("REVOKED","Revoked"),
                          ("DECEASED","Deceased"), )

LICENSE_TYPE_CHOICES =(   ("MD", "Medical Doctor (MD)"),
                          ("DO","Doctor of Osteopathy (DO)"),
                          ("PA","Physician Assistant"),
                          ("OTHER","Other"), )

class License(models.Model):
    number         = models.CharField(max_length=20, verbose_name="License Number",
                                                    db_index=True)
    state          = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATES, db_index=True)
    license_type   = models.CharField(max_length=5,  blank=True, default="",
                                    choices = LICENSE_TYPE_CHOICES, db_index=True)
    status         = models.CharField(max_length=10, choices=LICENSE_STATUS_CHOICES,
                                         default ="UNKNOWN")
    verified_by_issuing_board   = models.BooleanField(default=False)
    verified_by_ther_means      = models.BooleanField(default=False)
    verified                    = models.BooleanField(default=False, editable=False)
    note                        = models.TextField(max_length=255,  blank=True, default="")
    internal_note               = models.TextField(max_length=255,  blank=True, default="")
    note_restictions            = models.TextField(max_length=1024,  blank=True, default="")
    license_image               = models.ImageField(blank = True, null=False, default="",
                                    max_length=255L, upload_to="licenses-",
                                    verbose_name= "License Image",
                                    help_text= "PNG, JPG, or PDF formats accepted. 3MB max.")
    def save(self, **kwargs):
        if self.verified_by_issuing_board or self.verified_by_ther_means:
            self.verified=True
        else:
            self.verified=False        
        super(License, self).save(**kwargs)
    
    
    def __unicode__(self):
        r ="%s issued by %s is %s." % (self.number, self.state, self.status)
        return r

    def license_number(self):
        return self.number

        

class LicenseValidator(models.Model):

    state         = models.CharField(max_length=2, choices = US_STATES,
                                     unique=True)
    
    #license_type  = models.CharField(max_length=5,  blank=True, default="",
    #                                choices = LICENSE_TYPE_CHOICES)
    # the url will get following appended. No trailing slash. [/license/[state]/[number]
    url   = models.CharField(max_length=200, default ="")
    
    def __unicode__(self):
        return self.state
   