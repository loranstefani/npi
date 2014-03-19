from django.db import models
from django.conf import settings
from datetime import date
from ..taxonomy.models import TaxonomyCode
from django.contrib.auth.models import User
import uuid, random
from ..addresses.models import Address, US_STATE_CHOICES, US_STATE_W_FC_CHOICES
from ..addresses.countries import COUNTRIES
from ..licenses.models import License
from ..specialties.models import Specialty
from ..direct.models import DirectAddress, DirectCertificate
from ..identifiers.models import Identifier
from localflavor.us.models import PhoneNumberField


ENUMERATION_TYPE_CHOICES = (("NPI-1","Individual National Provider Identifier (NPI-1)"),
                            ("NPI-2","Organizational National Provider Identifier (NPI-2)"),
                            ("HPID","Health Plan Identifier (HPID)"),
                            ("OEID","Other Entity Individual Atypical Provider (OEID)"),)

ENUMERATION_STATUS_CHOICES  = (("P", "Pending"), ("A", "Active"), ("D", "Deactived"), )

DECACTIVAED_REASON_CHOICES = (("", "Blank"), ("DT", "Death"), ("DB", "Disbandment"),
                                ("FR", "Fraud"), ("OT", "Other"), )

ENTITY_CHOICES = (("INDIVIDUAL", "Individual"), ("ORGANIZATION", "Organization"))


INDIVIDUAL_OTHER_NAME_CHOICES = (("","Blank"), ("1","Former Name"),
                                ("2","Professional Name"),
                                ("5","Other Name"))

ORGANIZATION_OTHER_NAME_CHOICES = (("","Blank"), ("3","Doing Business As"),
                ("4","Former Legal Business Name"), ("5","Other Name"))


PREFIX_CHOICES = (('Ms.', 'Ms.'),('Mr.', 'Mr.'),('Miss','Miss'),
                  ('Mrs.','Mrs.'),('Dr.','Dr.'),('Prof.','Prof.'))


SUFFIX_CHOICES = (('Jr.','Jr.'),('Sr.','Sr.'),('I','I'),('II','II'),
                  ('III','III'),('IV','IV'),('V','V'),('VI','VI'),
                  ('VII','VII'),('VIII','VIII'),('IX','IX'),('X','X'),)

def generateUUID():
    return str(uuid.uuid4())

class Enumeration(models.Model):
    
    status                = models.CharField(max_length=1,
                                    choices=ENUMERATION_STATUS_CHOICES,
                                    default ="P", blank=True)
    enumeration_type            = models.CharField(max_length=5,
                                    choices=ENUMERATION_TYPE_CHOICES,)
        
    number              = models.CharField(max_length=10, blank=True, default="",
                                                   #editable=False,
                                                   db_index=True)
    enumeration_date    = models.DateField(blank=True, null=True, db_index=True)
    
    name_prefix         = models.CharField(choices=PREFIX_CHOICES, max_length=5, blank=True,
                                                   default="")
    first_name          = models.CharField(max_length=150, blank=True,
                                                   default="", db_index=True)
    middle_name          = models.CharField(max_length=150, blank=True,
                                                   default="")
    
    last_name           = models.CharField(max_length=150, blank=True,
                                                   default="", db_index=True)
    name_suffix           = models.CharField(choices=SUFFIX_CHOICES, max_length=4, blank=True,
                                                   default="")
    
    sole_proprietor         = models.BooleanField(default=False)
    organizational_subpart  = models.BooleanField(default=False)
    credential              = models.CharField(max_length=50, blank=True,
                                    default="", help_text ="e.g. MD, PA, OBGYN, DO")
    
    organization_name     = models.CharField(max_length=300, blank=True,
                                    default="", db_index=True,
                                    verbose_name="Legal Business Name")
    
    doing_business_as     = models.CharField(max_length=300, blank=True, default="")
     
    organization_other_name   = models.CharField(max_length=300, blank=True, default="")
    
    organization_other_name_code  = models.CharField(max_length=1, blank=True, default="",
                                    choices=ORGANIZATION_OTHER_NAME_CHOICES)
    
    other_first_name_1    = models.CharField(max_length=100, blank=True,
                                                   default="",
                                                   help_text="Previous First name")
    
    other_middle_name_1     = models.CharField(max_length=100, blank=True,
                                default="",
                                help_text="Another previous or maiden last name")
    
    
    other_last_name_1     = models.CharField(max_length=100, blank=True,
                                                   default="",
                                                   help_text="Previous or Maiden Last Name") 

    other_name_prefix_1     = models.CharField(choices=PREFIX_CHOICES, max_length=5, blank=True,
                                                   default="")
    
    other_name_suffix_1     = models.CharField(choices=SUFFIX_CHOICES, max_length=4, blank=True,
                                                   default="")

    other_name_credential_1     = models.CharField(max_length=20, blank=True,
                                                   default="")

    other_name_code_1  = models.CharField(max_length=1, blank=True, default="",
                                    choices=INDIVIDUAL_OTHER_NAME_CHOICES)
    other_first_name_2    = models.CharField(max_length=100, blank=True,
                                       default="",
                                       help_text="Another Previous first name")
    
    
    other_middle_name_2     = models.CharField(max_length=100, blank=True,
                                default="",
                                help_text="Another previous or maiden last name")
    
    
    other_last_name_2     = models.CharField(max_length=100, blank=True,
                                default="",
                                help_text="Another previous or maiden last name")
    
    other_name_prefix_2     = models.CharField(choices=PREFIX_CHOICES, max_length=5, blank=True,
                                                   default="")
    
    other_name_suffix_2     = models.CharField(choices=SUFFIX_CHOICES, max_length=4, blank=True,
                                                   default="")

    other_name_credential_2     = models.CharField(max_length=20, blank=True,
                                                   default="")

    other_name_code_2  = models.CharField(max_length=1, blank=True, default="",
                                    choices=INDIVIDUAL_OTHER_NAME_CHOICES)

    parent_organization         = models.ForeignKey('self', null=True, blank=True,
                                        related_name = "enumeration_parent_organization")
    
    parent_organization_legal_business_name  = models.CharField(max_length=300, default="", blank=True)
    parent_organization_ein     = models.CharField(max_length=10, default="", blank=True)
    
    #Profile Enhancements
    custom_profile_url         = models.CharField(max_length=100,   blank=True, default="",
                                                  db_index=True)
    website                    = models.CharField(max_length=200,   blank=True, default="")
    facebook_handle            = models.CharField(max_length=100,   blank=True, default="")
    twitter_handle             = models.CharField(max_length=100,   blank=True, default="")
    public_email               = models.EmailField(blank=True,      default="")
    driving_directions         = models.TextField(max_length=256,   blank=True, default="")
    bio_headline               = models.CharField(max_length=255,   blank=True, default="")
    bio_detail                 = models.TextField(max_length=1024,  blank=True, default="")
    background_image           = models.ImageField(blank = True,    null=False, default='',
                                    max_length=255L, upload_to="enumeration-backgrounds",
                                    verbose_name= "Background Image")
    avatar_image               = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="enumeration-avatars",
                                    verbose_name= "Avatar Photo")
    #PECOS Related
    pecos_id                    = models.CharField(max_length=20, blank=True,
                                                   default="")
    # Associations is stubbed out for future provider to organization or group relations.
    # This feature is not implemented, but wanted to create the DB model.
    associations                = models.ManyToManyField('self', null=True,
                                    blank=True, editable=False,
                                    related_name = "enumerations_associations")
    
    
    other_addresses             = models.ManyToManyField(Address,
                                    related_name = "enumeration_other_addresses",
                                    null=True, blank=True)
    
    mailing_address             = models.ForeignKey(Address,
                                    related_name = "enumeration_primary_mailing_address",
                                    verbose_name = "Mailing Address",
                                    null=True, blank=True)
    
    location_address            = models.ForeignKey(Address,
                                        help_text = "Location is a physical address of your practice or business",
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
    
    identifiers            = models.ManyToManyField(Identifier, null=True, blank=True,
                                        related_name ="enumeration_identifiers",
                                        db_index=True)
    
       
    taxonomy                   = models.ForeignKey(TaxonomyCode, null=True, blank=True,
                                        related_name ="enumeration_primary_taxonomy",
                                        verbose_name="Primary Taxonomy",
                                        db_index=True)
    
    other_taxonomies           = models.ManyToManyField(TaxonomyCode, null=True,
                                        blank=True, related_name ="enumeration_other_taxonomies")
    
    licenses                    = models.ManyToManyField(License, null=True, blank=True,
                                        related_name = "enumerations_licenses",
                                        db_index=True)
    
    specialties                 = models.ManyToManyField(Specialty, null=True, blank=True,
                                        related_name = "enumerations_specialties",
                                        db_index=True)
    
    direct_addresses            = models.ManyToManyField(DirectAddress, null=True, blank=True,
                                        related_name = "enumerations_direct_addresses",
                                        db_index=True)
    
    direct_certificates         = models.ManyToManyField(DirectCertificate, null=True, blank=True,
                                        related_name = "enumerations_direct_certificates",
                                        db_index=True)
    
    
    managers    = models.ManyToManyField(User, null=True, blank=True, db_index=True)
    

    #PII --------------------------------------------------------------------
    state_of_birth      = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATE_W_FC_CHOICES,
                        help_text="Choose Foriegn Country if the individual was not born in the US.")
    
    country_of_birth    = models.CharField(max_length=2,  blank=True, default="US",
                                    choices = COUNTRIES)
    
    birth_date          = models.DateField(blank=True, null=True,
                                           help_text="Format: YYYY-MM-DD")
    
    gender              = models.CharField(max_length=2,  blank=True, default="",
                                    verbose_name = "Sex",
                                    choices = (("F","Female"), ("M","Male"),
                                               ("T","Transgender")))
    
    itin        = models.CharField(max_length=10, blank=True,
                        default="", verbose_name="IRS Individual Tax Payer Identification Number (ITIN)",
                        help_text = "An ITIN is required for individuals that are not eligible for a social security number (SSN).",
                        db_index=True)
    
    ssn          = models.CharField(max_length=10, blank=True, default="",
                        verbose_name = "Social Security Number (SSN)",
                        help_text= "Required for individuals unless an ITIN is provided",
                        db_index=True)

    ein         = models.CharField(max_length=9, blank=True,
                    default="", verbose_name="Employer Identification Number (EIN)",
                    help_text = "An EIN is issued by the IRS. This is required for organizations.",
                    db_index=True)

    ein_image   = models.ImageField(blank = True, null=False, default='',
                    max_length=255L, upload_to="ein-verification",
                    verbose_name= "EIN Image",
                    help_text ="A PDF or PNG of your EIN assigned by the IRS",)
    
    modify_token  = models.CharField(max_length=36, blank=True, default=generateUUID)
   
    
    national_agency_check = models.BooleanField(default=False)
    fingerprinted         = models.BooleanField(default=False)
    negative_action       = models.BooleanField(default=False,
                                 verbose_name="Negative Action on file with HRSA")
    
    #Deactivation information ---------------------------
    deactivation_reason_code  = models.CharField(max_length=2,
                                    choices=DECACTIVAED_REASON_CHOICES,
                                    default="", blank=True)
    deactivated_details = models.TextField(max_length=1000, blank=True, default="")

    deactivation_date  = models.DateField(blank=True, null=True)
    reactivation_date   = models.DateField(blank=True, null=True)
    replacement_npi     = models.CharField(max_length=10,blank=True, default="")
    
    
    contact_person_email        = models.EmailField(blank=True, default="",
                                    help_text = "Required if contact person has an email.",
                                    db_index=True)
    contact_person_first_name  = models.CharField(max_length=150,
                                                  blank=True, default="")
    contact_person_middle_name = models.CharField(max_length=150,
                                                  blank=True, default="")
    contact_person_last_name   = models.CharField(max_length=150,
                                                  blank=True, default="")
    
    contact_person_prefix   = models.CharField(choices=PREFIX_CHOICES,
                                    max_length=5, blank=True, default="")
    
    contact_person_suffix   = models.CharField(choices=SUFFIX_CHOICES, max_length=4,
                                    blank=True, default="")

    contact_person_credential    = models.CharField(max_length=20, blank=True,
                                        default="",
                                        help_text="e.g. PhD, RN, MD")
    
    contact_person_title_or_position   = models.CharField(max_length=150,
                                            blank=True, default="")
    
    contact_person_telephone_number   = PhoneNumberField(max_length=12,
                                                         blank=True, default="",
                                           help_text="Format: XXX-XXX-XXXX.")
    contact_person_telephone_extension   = models.CharField(max_length=10,
                                                  blank=True, default="")
    contact_person_title_or_position       = models.CharField(max_length=150,
                                                  blank=True, default="")

    contact_person_title       = models.CharField(max_length=150,
                                                  blank=True, default="")
    
    authorized_official_email = models.EmailField(blank=True, default="",
                               help_text = "Required if the authorized official has an email.",
                               db_index=True)
    
    # End PII -----------------------------------------------------------------
    authorized_official_prefix        = models.CharField(choices=PREFIX_CHOICES, max_length=10,
                                            blank=True, default="",
                                            help_text = "For example, Mr., Ms., Mrs., Dr.")
    authorized_official_first_name    = models.CharField(max_length=150,
                                            blank=True, default="")
    authorized_official_middle_name   = models.CharField(max_length=150,
                                            blank=True, default="")
    authorized_official_last_name     = models.CharField(max_length=150,
                                            blank=True, default="")
    authorized_official_suffix  = models.CharField(choices=SUFFIX_CHOICES,
                                        max_length=4, blank=True, default="")
    
    authorized_official_credential    = models.CharField(max_length=20,
                                            blank=True, default="")
    
    authorized_official_title_or_position  = models.CharField(max_length=150,
                                                  blank=True, default="",)
    
    authorized_official_telephone_number   = PhoneNumberField(max_length=12,  blank=True, default="",
                                            help_text="Format: XXX-XXX-XXXX.")
    
    authorized_official_telephone_extension  = models.CharField(max_length=10,
                                                  blank=True, default="")
    
    authorized_official_title_or_position     = models.CharField(max_length=150,
                                                  blank=True, default="")
    
    authorized_official_title      = models.CharField(max_length=150,blank=True,
                                                      default="")

    #Record management
    last_updated        = models.DateField(blank=True, null=True)
    added               = models.DateField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)


    class Meta:
        get_latest_by = "id"
        ordering = ('-enumeration_date',)



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
        
        #Set the DBA
        if self.organization_other_name and self.organization_other_name_code=="3" and \
           not self.doing_business_as:
            self.doing_business_as = self.organization_other_name
        
        
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
    