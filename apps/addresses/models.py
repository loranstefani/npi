from django.db import models
from localflavor.us.models import PhoneNumberField
from localflavor.us.us_states import US_STATES
from countries import COUNTRIES

US_STATE_CHOICES = list(US_STATES)
US_STATE_CHOICES.insert(0, ('', 'Please Choose a State'))
US_STATE_CHOICES.append(('AE', 'AE - (ZIPs 09xxx) Armed Forces Europe which includes Canada, Middle East, and Africa'))
US_STATE_CHOICES.append(('AP', 'AP - (ZIPs 962xx) Armed Forces Pacific'))
US_STATE_CHOICES.append(('AA', 'AA - (ZIPs 340xx) Armed Forces (Central and South) Americas'))
US_STATE_CHOICES.append(('ZZ', 'Foreign Country'))



ADDRESS_TYPE_CHOICES    = (("DOM", "Domsestic"),                           
                           ("FGN", "Foreign"),
                           ("MIL", "Military"),
                        )


ADDRESS_PURPOSE_CHOICES = (("LOCATION",     "Location Address (Phyiscal)"),
                           ("MAILING",      "Mailing Address (Correspondence)"),
                           ("MEDREC-STORAGE",       "Medical Records Storage Address"),
                           ("1099",                 "1099 Address"),
                           ("REVALIDATION",         "Revalidation Address"),
                           ("ADDITIONAL-LOCATION",  "Additional Location Address"),)


#AE (ZIPs 09xxx) for Armed Forces Europe which includes Canada, Middle East, and Africa
#AP (ZIPs 962xx - 966xx) for Armed Forces Pacific
#AA (ZIPs 340xx) for Armed Forces (Central and South) Americas

MPO_CHOICES = ( ('APO',  'APO - Army/Air Post Office'),
                ('FPS',  'FPS - Fleet Post Office'),
                ('DPO',  'PDO - Diplomatic Post Office'))



class Address(models.Model):
    address_type    = models.CharField(max_length=12, choices=ADDRESS_TYPE_CHOICES)
    address_purpose = models.CharField(max_length=20, choices=ADDRESS_PURPOSE_CHOICES)
    address_1       = models.CharField(max_length=200, default="")
    address_2       = models.CharField(max_length=200, blank=True, default="")
    city            = models.CharField(max_length=200, blank=True, default="")
    state           = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATE_CHOICES)
    zip             = models.CharField(max_length=10,  blank=True, default="")
    country_code    = models.CharField(max_length=2,  blank=True, default="US",
                                    choices = COUNTRIES)
    foreign_state         = models.CharField(max_length=2,  blank=True, default="")
    foreign_postal        = models.CharField(max_length=12,  blank=True, default="")
    us_telephone_number   = PhoneNumberField(max_length=12,  blank=True, default="",
                                           help_text="Format: XXX-XXX-XXXX. Required if the address has a telephone."
                                           )
    us_fax_number   = models.CharField(max_length=12,  blank=True, default="",)
    foreign_telephone_number   = models.CharField(max_length=20,  blank=True, default="")
    foreign_fax_number   = models.CharField(max_length=20,  blank=True, default="") 
    mpo                    = models.CharField(max_length=3, choices= MPO_CHOICES,
                                              blank=True, default="",
                                              verbose_name="Military Post Office")
    latitude                = models.CharField(max_length=20, default="", blank=True)
    longitude               = models.CharField(max_length=20, default="", blank=True)
    website                 = models.CharField(max_length=15,  blank=True, default="")
    driving_details         = models.CharField(max_length=15,  blank=True, default="")
    hours_of_operation      = models.TextField(max_length=255,  blank=True, default="")
    private_email_contact   = models.CharField(max_length=15,  blank=True, default="")
    public_email_contact    = models.CharField(max_length=15,  blank=True, default="")
    phone_number_extension  = models.CharField(max_length=15,  blank=True, default="")
    diplay_phone            = models.BooleanField(default=False)
    display_fax             = models.BooleanField(default=False)
    usps_stadardized        = models.BooleanField(default=False)
    ignore_standardized     = models.BooleanField(default=False,
                            help_text="Check this if the USPS is just wrong and causes missed correspondence.")
    background_image            = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="address-backgrounds",
                                    verbose_name= "Background Image")
    
    avatar_image                = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="address-avatars",
                                    verbose_name= "Profile Photo")

    def __unicode__(self):
        
        address = "address object"
        if self.address_type == "DOM":
            address = "%s %s %s, %s %s %s" % (self.address_1, self.address_2, self.city,
                                          self.state, self.zip, self.country_code)
            
        if self.address_type == "FGN":
            address = "%s %s %s, %s %s %s" % (self.address_1, self.address_2, self.city,
                                          self.foreign_state, self.foreign_postal,
                                          self.country_code)

        if self.address_type == "MIL":
            address = "%s %s %s %s %s" % (self.address_1, self.address_2,
                                                   self.mpo, self.state, self.zip,)
        return address      
       

    
    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)
        verbose_name_plural = "Addresses"




    def save(self, **kwargs):
        if self.zip.startswith("09"):
            self.state ="AE"
            
        if self.zip.startswith("962"):
            self.state ="AP"
        
        if self.zip.startswith("340"):
            self.state ="AA"
     
        super(Address, self).save(**kwargs)
