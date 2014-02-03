from django.db import models
from django.conf import settings
from datetime import date
from ..taxonomy.models import TaxonomyCode
from django.contrib.auth.models import User
import uuid, random
from ..addresses.models import Address, US_STATE_CHOICES
from ..addresses.countries import COUNTRIES
from ..licenses.models import License
from ..direct.models import DirectAddress
from localflavor.us.models import PhoneNumberField


ENUMERATION_TYPE_CHOICES = (("NPI-1","Individual National Provider Identifier (NPI-1)"),
                            ("NPI-2","Organizational National Provider Identifier (NPI-2)"),
                            ("HPID","Health Plan Identifier (HPID)"),
                            ("OEID","Other Entity Individual Atypical Provider (OEID)"),
                            )

ENUMERATION_STATUS_CHOICES  = (("P", "Pending"), ("A", "Active"), ("D", "Deactived"), )

DECACTIVAED_REASON_CHOICES = (("", "Blank"), ("D", "Deceased"), ("F", "Fraud"),
                              ("O", "Other"), )


ENTITY_CHOICES = (("INDIVIDUAL", "Individual"), ("ORGANIZATION", "Organization"))


COUNTRY_CHOICES = (("US", "United States"), ("CA", "Canada"), ("MX", "Mexico"))



class Enumeration(models.Model):
    
    status                = models.CharField(max_length=1,
                                    choices=ENUMERATION_STATUS_CHOICES,
                                    default ="P", blank=True)
        
    number              = models.CharField(max_length=10, blank=True, default="",
                                                   #editable=False
                                                   )
    enumeration_date    = models.DateField(blank=True, null=True)
    
    name_prefix         = models.CharField(max_length=10, blank=True,
                                                   default="")
    first_name          = models.CharField(max_length=100, blank=True,
                                                   default="")
    middle_name          = models.CharField(max_length=100, blank=True,
                                                   default="")
    
    last_name           = models.CharField(max_length=100, blank=True,
                                                   default=
                                                   "")
    name_suffix           = models.CharField(max_length=15, blank=True,
                                                   default="")
    
    credential           = models.CharField(max_length=15, blank=True,
                                                   default="",
                                                   help_text ="e.g. MD, PA, OBGYN, DO")
    
    organization_name     = models.CharField(max_length=150, blank=True,
                                                   default="")
    
    doing_business_as     = models.CharField(max_length=150, blank=True, default="")
     
    
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
    

    public_email               = models.CharField(max_length=150,  blank=True, default="")
    
    taxonomy                   = models.ForeignKey(TaxonomyCode, null=True, blank=True,
                                        related_name ="enumeration_primary_taxonomy",
                                        verbose_name="Primary Taxonomy")
    other_taxonomies           = models.ManyToManyField(TaxonomyCode, null=True,
                                        blank=True, related_name ="enumeration_other_taxonomies")
    
    #Profile Enhancements
    website                    = models.CharField(max_length=300,   blank=True, default="")
    facebook_handle            = models.CharField(max_length=300,   blank=True, default="")
    twitter_handle             = models.CharField(max_length=300,   blank=True, default="")
    public_email               = models.EmailField(blank=True,      default="")
    driving_directions         = models.TextField(max_length=256,   blank=True, default="")
    hours_of_operation         = models.TextField(max_length=256,   blank=True, default="")
    bio_headline               = models.CharField(max_length=255,   blank=True, default="")
    bio_detail                 = models.TextField(max_length=1024,  blank=True, default="")
    background_image           = models.ImageField(blank = True,    null=False, default='',
                                    max_length=255L, upload_to="enumeration-backgrounds",
                                    verbose_name= "Background Image")
    
    avatar_image               = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="enumeration-avatars",
                                    verbose_name= "Avatar Photo")
    
    image_left                 = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="image_left",
                                    verbose_name= "Left Profile Photo")
    
    image_right                = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="image_right",
                                    verbose_name= "Right Profile Photo")


    medicare_id                 = models.CharField(max_length=20, blank=True, default="")
    

    managers                    = models.ManyToManyField(User, null=True, blank=True)
    

    other_addresses             = models.ManyToManyField(Address,
                                    related_name = "enumeration_other_addresses",
                                    null=True, blank=True)
    

    mailing_address             = models.ForeignKey(Address,
                                    related_name = "enumeration_primary_mailing_address",
                                    verbose_name = "Business address for correspondence",
                                    null=True, blank=True)
    
    location_address    = models.ForeignKey(Address,
                            help_text = "Primary location (a physical address of your practice or business",
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

    
    tracking_number             = models.CharField(max_length=50, blank=True, default="")
    

    

    sole_proprietor             = models.BooleanField(default=False)

    #PII
    state_of_birth      = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATE_CHOICES)
    
    country_of_birth    = models.CharField(max_length=2,  blank=True, default="US",
                                    choices = COUNTRIES)
    
    birth_date          = models.DateField(blank=True, null=True)
    
    gender              = models.CharField(max_length=2,  blank=True, default="",
                                    choices = (("F","Female"), ("M","Male"),
                                               ("T","Transgender")))
    
    
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
   
    

    #CMS System of Record - Private information
    national_agency_check = models.BooleanField(default=False)
    fingerprinted         = models.BooleanField(default=False)
    negative_action       = models.BooleanField(default=False,
                                 verbose_name="Negative Action on file with HRSA")
    
    contact_person_email        = models.EmailField(blank=True, default="",
                                    help_text = "Required if contact person has an email.")
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
    
    contact_person_title_or_position   = models.CharField(max_length=150,
                                                  blank=True, default="",
                                                  help_text = "For example, Jr., Sr., II, III."
                                                  )
    
    contact_person_telephone_number   = PhoneNumberField(max_length=12,  blank=True, default="",
                                           help_text="Format: XXX-XXX-XXXX."
                                           )
    contact_person_telephone_extension   = models.CharField(max_length=10,
                                                  blank=True, default="")
    contact_person_title_or_position       = models.CharField(max_length=150,
                                                  blank=True, default="")

    contact_person_title       = models.CharField(max_length=150,
                                                  blank=True, default="")
    
    authorized_person_email = models.EmailField(blank=True, default="",
                               help_text = "Required if authorized person has an email.")
    
    # End PII ---------------------------------------------------

    authorized_person_first_name    = models.CharField(max_length=150,
                                            blank=True, default="")
    authorized_person_middle_name   = models.CharField(max_length=150,
                                            blank=True, default="")
    authorized_person_last_name     = models.CharField(max_length=150,
                                            blank=True, default="")
    authorized_person_suffix        = models.CharField(max_length=150,
                                            blank=True, default="",
                                            help_text = "For example, Jr., Sr., II, III.")
    
    authorized_person_title_or_position  = models.CharField(max_length=150,
                                                  blank=True, default="",)
    
    authorized_person_telephone_number   = PhoneNumberField(max_length=12,  blank=True, default="",
                                            help_text="Format: XXX-XXX-XXXX.")
    
    authorized_person_telephone_extension   = models.CharField(max_length=10,
                                                  blank=True, default="")
    
    authorized_person_title_or_position       = models.CharField(max_length=150,
                                                  blank=True, default="")
    
    authorized_person_title       = models.CharField(max_length=150,
                                                  blank=True, default="")


    #Deactivation information
    decactvation_reason_code  = models.CharField(max_length=1, choices=DECACTIVAED_REASON_CHOICES,
                                    default="", blank=True)
    deactivated_details         = models.TextField(max_length=1000, blank=True, default="")

    deactiviation_date               = models.DateField(blank=True, null=True)
    reactiviation_date               = models.DateField(blank=True, null=True)
    
    
    #Record management
    added               = models.DateField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)


    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)



    def name(self):
        name = "Not Provided"
        if self.enumeration_type in ("HPID", "OEID", "NPI-2"):
            name = self.organization_name
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as,
                                    self.organization_name)
        elif self.enumeration_type in ("NPI-1", ):
            name = "%s %s" % (self.first_name, self.last_name)
            if self.doing_business_as:
                name = "%s %s (%s)" % (self.first_name,
                                       self.last_name,
                                       self.doing_business_as,)

        if not name or name== " ":
            return "Not Provided"
        return name



    def entity_type(self):
        entity_type = None
        if self.enumeration_type in ("HPID", "OEID", "NPI-2"):
            entity_type = "Organization"
        elif self.enumeration_type in ("NPI-1",):
            entity_type = "Individual"
        return entity_type
    

    def entity_type_code(self):
        entity_type = None
        if self.enumeration_type in ("HPID", "OEID", "NPI-2"):
            entity_type = "2"
        elif self.enumeration_type in ("NPI-1",):
            entity_type = "1"
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
    
    def google_map_q(self):
        
        address_plus = str(self.location_address).replace(" ", "+")
        return address_plus
    


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
            self.enumeration_date = date.today()
            
        super(Enumeration, self).save(**kwargs)
    