from django.db import models
from localflavor.us.models import PhoneNumberField
from localflavor.us.us_states import US_STATES
from countries import COUNTRIES

US_STATE_CHOICES = list(US_STATES)
US_STATE_CHOICES.insert(0, ('', 'Please Choose a State'))
US_STATE_CHOICES.extend(
    [('AS', 'American Samoa'),
    ('FM', 'Micronesia, Federated states of'),
    ('GU', 'Guam'),
    ('MH', 'Marshall Islands'),
    ('MP', 'Mariana Islands, Northern'),
    ('PR', 'Puerto Rico'),
    ('PW', 'Palau'),
    ('VI', 'Virgin Islands')])

MILITARY_STATE_CHOICES = [('AE', 'AE - (ZIPs 09xxx) Armed Forces Europe which includes Canada, Middle East, and Africa'),
    ('AP', 'AP - (ZIPs 962xx) Armed Forces Pacific'),
    ('AA', 'AA - (ZIPs 340xx) Armed Forces (Central and South) Americas'),
    ]


FOREIGN_COUTRY_STATE_CHOICES = [('ZZ', 'Foreign Country')]



US_STATE_CHOICES_ALL = US_STATE_CHOICES + MILITARY_STATE_CHOICES + FOREIGN_COUTRY_STATE_CHOICES



ADDRESS_TYPE_CHOICES    = (("DOM", "Domsestic"),                           
                           ("FGN", "Foreign"),
                           ("MIL", "Military"),
                        )


ADDRESS_PURPOSE_CHOICES = (("LOCATION",     "Location Address (Phyiscal)"),
                           ("MAILING",      "Mailing Address (Correspondence)"),
                           ("MEDREC-STORAGE",       "Medical Records Storage Address"),
                           ("1099",                 "1099 Address"),
                           ("REVALIDATION",         "Revalidation Address"),
                           ("ADDITIONAL-LOCATION",  "Additional Location Address"),
                           ("REMITTANCE",            "Remmitance Address"),
                           )


MPO_CHOICES = ( ('APO',  'APO - Army/Air Post Office'),
                ('FPS',  'FPS - Fleet Post Office'),
                ('DPO',  'PDO - Diplomatic Post Office'))





class Address(models.Model):
    address_type    = models.CharField(max_length=12, choices=ADDRESS_TYPE_CHOICES)
    address_purpose = models.CharField(max_length=20, choices=ADDRESS_PURPOSE_CHOICES)
    address_1       = models.CharField(max_length=200, default="", db_index=True)
    address_2       = models.CharField(max_length=200, blank=True, default="")
    city            = models.CharField(max_length=200, blank=True, default="")
    state           = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATE_CHOICES_ALL)
    zip             = models.CharField(max_length=10,  blank=True, default="")
    country_code    = models.CharField(max_length=2,  blank=True, default="US",
                                    choices = COUNTRIES)
    foreign_state         = models.CharField(max_length=2,  blank=True, default="")
    foreign_postal        = models.CharField(max_length=12,  blank=True, default="")
    us_telephone_number   = PhoneNumberField(max_length=12,  blank=True, default="",
                                           help_text="Format: XXX-XXX-XXXX. Required if the address has a telephone.")
    
    telephone_number_extension   = models.CharField(max_length=10,  blank=True, default="")
    
    us_fax_number   = models.CharField(max_length=12,  blank=True, default="",)
    foreign_telephone_number   = models.CharField(max_length=20,  blank=True, default="")
    foreign_fax_number   = models.CharField(max_length=20,  blank=True, default="") 
    mpo             = models.CharField(max_length=3, choices= MPO_CHOICES,
                                              blank=True, default="",
                                              verbose_name="Military Post Office")
    
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
     
     
    county_name             = models.CharField(max_length=150,  blank=True, default="")
    active                  = models.CharField(max_length=2,  blank=True, default="")
    deliverable             = models.CharField(max_length=2,  blank=True, default="")
    vacant                  = models.CharField(max_length=2,  blank=True, default="")
    record_type             = models.CharField(max_length=2,  blank=True, default="")
    rdi                     = models.CharField(max_length=15,  blank=True, default="")
    lat                     = models.CharField(max_length=20, default="", blank=True)
    long                    = models.CharField(max_length=20, default="", blank=True)                                             
                                                  
                                                  
                           

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
