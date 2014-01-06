from django.db import models
from django.conf import settings
from ..taxonomy.models import TaxonomyCode
from django.contrib.auth.models import User
import uuid
from localflavor.us.us_states import US_STATES
import random
from countries import COUNTRIES
from ..licenses.models import License
from ..direct.models import DirectAddress
from localflavor.us.models import PhoneNumberField
US_STATE_CHOICES = list(US_STATES)
US_STATE_CHOICES.insert(0, ('', 'Please Choose a State'))
US_STATE_CHOICES.append(('AE', 'AE - (ZIPs 09xxx) Armed Forces Europe which includes Canada, Middle East, and Africa'))
US_STATE_CHOICES.append(('AP', 'AP - (ZIPs 962xx) Armed Forces Pacific'))
US_STATE_CHOICES.append(('AA', 'AA - (ZIPs 340xx) Armed Forces (Central and South) Americas'))
US_STATE_CHOICES.append(('ZZ', 'Foreign Country'))


#AE (ZIPs 09xxx) for Armed Forces Europe which includes Canada, Middle East, and Africa
#AP (ZIPs 962xx - 966xx) for Armed Forces Pacific
#AA (ZIPs 340xx) for Armed Forces (Central and South) Americas

ENUMERATION_TYPE_CHOICES = (("NPI-1","Individual National Provider Identifier (NPI-1)"),
                            ("NPI-2","Organizational National Provider Identifier (NPI-2)"),
                            ("HPID","Health Plan Identifier (HPID)"),
                            ("OEID","Other Entity Individual Atypical Provider (OEID)"),
                        )

ENUMERATION_STATUS_CHOICES  = (("P", "Pending"), ("A", "Active"), ("D", "Deactived"), )

DECACTIVAED_REASON_CHOICES = (("", "Blank"), ("D", "Deceased"), ("F", "Fraud"),
    ("O", "Other"), )

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
                        )


ENTITY_CHOICES = (("INDIVIDUAL", "Individual"), ("ORGANIZATION", "Organization"))


COUNTRY_CHOICES = (("US", "United States"), ("CA", "Canada"), ("MX", "Mexico"))


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
    bio                     = models.TextField(max_length=255,  blank=True, default="")
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

class Enumeration(models.Model):
    
    number              = models.CharField(max_length=10, blank=True, default="",
                                                   #editable=False
                                                   )
    enumeration_date    = models.DateField(auto_now_add=True)
    
    name_prefix         = models.CharField(max_length=10, blank=True,
                                                   default="")
    first_name          = models.CharField(max_length=100, blank=True,
                                                   default="")
    middle_name          = models.CharField(max_length=100, blank=True,
                                                   default="")
    
    last_name           = models.CharField(max_length=100, blank=True,
                                                   default=
                                                   "")
    state_of_birth      = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATE_CHOICES)
    
    country_of_birth    = models.CharField(max_length=2,  blank=True, default="US",
                                    choices = COUNTRIES)
    
    
    name_suffix           = models.CharField(max_length=10, blank=True,
                                                   default="")
    organization_name     = models.CharField(max_length=100, blank=True,
                                                   default="")
    doing_business_as     = models.CharField(max_length=100, blank=True, default="")
     
    other_first_name_1    = models.CharField(max_length=100, blank=True,
                                                   default="",
                                                   help_text="Previous first name")
    
    other_last_name_1     = models.CharField(max_length=100, blank=True,
                                                   default="",
                                                   help_text="Previous or maiden last name") 
    
    other_first_name_2    = models.CharField(max_length=100, blank=True,
                                       default="",
                                       help_text="Another previous first name")
    
    other_last_name_2     = models.CharField(max_length=100, blank=True,
                                                   default="",
                                                   help_text="Another previous or maiden last name")
    
    status                = models.CharField(max_length=1,
                                    choices=ENUMERATION_STATUS_CHOICES,
                                    default ="P", blank=True)
    
    medicare_id                 = models.CharField(max_length=20, blank=True, default="")
    
    managers                    = models.ManyToManyField(User, null=True, blank=True)
    
    other_addresses             = models.ManyToManyField(Address,
                                    related_name = "enumeration_other_addresses",
                                    null=True, blank=True)
    
    mailing_address             = models.ForeignKey(Address,
                                    related_name = "enumeration_primary_mailing_address",
                                    verbose_name = "Business address for correspondence",
                                    null=True, blank=True)
    
    location_address            = models.ForeignKey(Address,
                                    help_text = "Primary location (a physical adrress of your practice or business",
                                    related_name = "enumeration_location_address",
                                    null=True, blank=True)
    
    medical_record_storage_address  = models.ForeignKey(Address,
                                    related_name = "enumeration_medical_record_storage_address",
                                    null=True, blank=True)
    
    correspondence_address    = models.ForeignKey(Address,
                                    related_name = "enumeration_correspondence_address",
                                    null=True, blank=True)
    
    ten_ninety_nine_address = models.ForeignKey(Address, verbose_name="1099 Address",
                                    related_name = "enumeration_ten_ninety_nine_address",
                                    null=True, blank=True)
    
    revalidation_address    = models.ForeignKey(Address, verbose_name="PECOS Revalidation Address",
                                    related_name = "enumeration_revalidation_address",
                                    null=True, blank=True)
   
    parent_organization         = models.ForeignKey('self', null=True, blank=True,
                                    related_name = "enumeration_parent_organization")
    
    associations                = models.ManyToManyField('self', null=True, blank=True,
                                    related_name = "enumerations_associations")
    enumeration_type            = models.CharField(max_length=10, choices=ENUMERATION_TYPE_CHOICES,)
    
    licenses                    = models.ManyToManyField(License, null=True, blank=True,
                                    related_name = "enumerations_licenses")
    direct_addresses            = models.ManyToManyField(DirectAddress, null=True, blank=True,
                                    related_name = "enumerations_direct_addresses")
    #entity_type                 = models.CharField(max_length=12, choices=ENTITY_CHOICES)
    tracking_number             = models.CharField(max_length=50, blank=True, default="")
    
    decactvation_reason_code          = models.CharField(max_length=1, choices=DECACTIVAED_REASON_CHOICES,
                                    default="", blank=True)
    
    deactivated_details         = models.TextField(max_length=1000, blank=True, default="")
    

    sole_protieter              = models.BooleanField(default=False, editable=False)
    sole_proprietor             = models.BooleanField(default=False)

    itin                        = models.CharField(max_length=10, blank=True,
                                        default="", verbose_name="IRS Individual Tax Payer  Number (ITIN)",
                                        help_text = "An ITIN is required for individuals that are not eligible for a social security number."
                                        )
    ssn                         = models.CharField(max_length=10, blank=True, default="",
                                        verbose_name = "Social Security Number",
                                        help_text= "Required for individuals.")

    ein                        = models.CharField(max_length=9, blank=True,
                                        default="", verbose_name="Employer Identification Number (EIN)",
                                        help_text = "An EIN is issued by the IRS. This is required for organizations and optional for individuals."
                                        )

    ein_image               = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="ein-verification",
                                    verbose_name= "EIN Image",
                                    help_text ="A PDF or PNG of your EIN assigned by the IRS",
                                    )
    
    modify_token               = models.CharField(max_length=36, blank=True, default=uuid.uuid4)
   
    public_email               = models.CharField(max_length=150,  blank=True, default="")
    taxonomy                   = models.ForeignKey(TaxonomyCode, null=True, blank=True,
                                        related_name ="enumeration_primary_taxonomy")
    other_taxonomies           = models.ManyToManyField(TaxonomyCode, null=True,
                                        blank=True, related_name ="enumeration_other_taxonomies")
    website                    = models.CharField(max_length=300,  blank=True, default="")
    
    public_email               = models.EmailField(blank=True, default="")
    driving_directions         = models.TextField(max_length=266,  blank=True, default="")
    hours_of_operation         = models.CharField(max_length=15,  blank=True, default="")
   
    phone_number_extension     = models.CharField(max_length=15,  blank=True, default="")
    bio                        = models.TextField(max_length=255,  blank=True, default="")
    national_agency_check      = models.BooleanField(default=False)
    
    fingerprinted              = models.BooleanField(default=False)
    
    negative_action            = models.BooleanField(default=False,
                                    verbose_name="Negative Action on file with HRSA")
    
    background_image           = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="enumeration-backgrounds",
                                    verbose_name= "Background Image")
    
    avatar_image               = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="enumeration-avatars",
                                    verbose_name= "Profile Photo")

    contact_person_email       = models.EmailField(blank=True, default="")
    contact_person_first_name  = models.CharField(max_length=150,
                                                  blank=True, default="")
    contact_person_middle_name = models.CharField(max_length=150,
                                                  blank=True, default="")
    contact_person_last_name   = models.CharField(max_length=150,
                                                  blank=True, default="")
    contact_person_suffix      = models.CharField(max_length=150,
                                                  blank=True, default="",
                                                  help_text = "For example, M.D., R.N., PhD"
                                                  )
    
    contact_person_credential   = models.CharField(max_length=150,
                                                  blank=True, default="",
                                                  help_text = "For example, Jr., Sr., II, III."
                                                  )
    
    contact_person_telephone_number   = PhoneNumberField(max_length=12,  blank=True, default="",
                                           help_text="Format: XXX-XXX-XXXX. Required if the address has a telephone."
                                           )
    contact_person_telephone_extension   = models.CharField(max_length=10,
                                                  blank=True, default="")
    contact_person_title_or_position       = models.CharField(max_length=150,
                                                  blank=True, default="")

    contact_person_title       = models.CharField(max_length=150,
                                                  blank=True, default="")

    authorized_person_email      = models.EmailField(blank=True, default="")
    authorized_person_first_name  = models.CharField(max_length=150,
                                                  blank=True, default="")
    authorized_person_middle_name = models.CharField(max_length=150,
                                                  blank=True, default="")
    authorized_person_last_name   = models.CharField(max_length=150,
                                                  blank=True, default="")
    authorized_person_suffix      = models.CharField(max_length=150,
                                                  blank=True, default="",
                                                  help_text = "For example, M.D., R.N., PhD"
                                                  )
    
    authorized_person_credential   = models.CharField(max_length=150,
                                                  blank=True, default="",
                                                  help_text = "For example, Jr., Sr., II, III."
                                                  )
    
    authorized_person_telephone_number   = PhoneNumberField(max_length=12,  blank=True, default="",
                                            help_text="Format: XXX-XXX-XXXX. Required if the authorized person has a telephone.")
    authorized_person_telephone_extension   = models.CharField(max_length=10,
                                                  blank=True, default="")
    
    authorized_person_title_or_position       = models.CharField(max_length=150,
                                                  blank=True, default="")
    authorized_person_title       = models.CharField(max_length=150,
                                                  blank=True, default="")

    added               = models.DateField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)


    deactiviation_date               = models.DateField(auto_now_add=True)
    reactiviation_date               = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)



    def name(self):
        name = "UNK"
        if self.enumeration_type in ("HPID", "OEID-2", "NPI-2"):
            name = self.organization_name
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as,
                                    self.organization_name)
        elif self.enumeration_type in ("OEID-1", "NPI-1"):
            name = "%s %s" % (self.first_name, self.last_name)
            if self.doing_business_as:
                name = "%s (%s %s)" % (self.doing_business_as,
                                    self.first_name,
                                    self.last_name)

        if not name or name== " ":
            return "UNK"
        return name



    def entity_type(self):
        entity_type = None
        if self.enumeration_type in ("HPID", "OEID-2", "NPI-2"):
            entity_type = "Organization"
        elif self.enumeration_type in ("OEID-1", "NPI-1"):
            entity_type = "Individual"
        return entity_type
    
    
    def pretty_status(self):
        pretty_status = None
        if str(self.status) == "A":
            pretty_status = "Active"
        
        if str(self.status) == "P":
            pretty_status = "Pending"   
    
        if str(self.status) == "D":
            pretty_status = "Decactivated"   
    
        return pretty_status
    
    
    def pretty_number(self):
        if not self.number:
            return  "Unassigned"
           
        return self.number


    def detail(self):
        name = "UNK"
        if self.enumeration_type in ("HPID", "OEID-2", "NPI-2"):
            name = self.organization_name
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as,
                                    self.organization_name)
        elif self.enumeration_type in ("OEID-1", "NPI-1"):
            name = "%s %s" % (self.first_name, self.last_name)
            if self.doing_business_as:
                name = "%s (%s %s)" % (self.doing_business_as,
                                    self.first_name,
                                    self.last_name)
        number=self.number
        if not number:
            number = "NOT-ASSIGNED"
        managers = ", ".join([manager.username for manager in self.managers.all()])
        if not managers:
            managers = "no one"
        if not name:
            name = "Name, No"
        
        
        e = "%s %s is an %s managed by %s." % (number, name,
                                               self.enumeration_type,
                                              managers)
        return e



    def __unicode__(self):
        name = "No Name"
        if self.enumeration_type in ("HPID", "OEID-2", "NPI-2"):
            name = self.organization_name
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as,
                                    self.organization_name)
        elif self.enumeration_type in ("OEID-1", "NPI-1"):
            name = "%s %s" % (self.first_name, self.last_name)
            if self.doing_business_as:
                name = "%s (%s %s)" % (self.doing_business_as,
                                    self.first_name,
                                    self.last_name)
        number=self.number
        if not number:
            number = "Unassigned"
            
        e = "%s/%s/%s" % (self.enumeration_type, number, name)
        return e




    def save(self, **kwargs):
        #If the status is active but no enumeration number is assigned then create one.
        if self.status == "A" and self.number == "":
            if self.enumeration_type in ("NPI-1", "NPI-2"):
                self.number = random.randrange(100000000,199999999)
            if self.enumeration_type in ("HPID-2"):
                self.number = random.randrange(7000000000,7999999999)
             
            if self.enumeration_type in ("OEID-1", "OEID-2"):
                self.number = random.randrange(6000000000,6999999999)   
            
        super(Enumeration, self).save(**kwargs)
    