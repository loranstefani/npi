from django.db import models
from django.conf import settings
from datetime import date
from ..taxonomy.models import TaxonomyCode
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
import uuid, random
from utils import valid_uuid
from ..addresses.models import Address, US_STATE_CHOICES, US_STATE_W_FC_CHOICES
from ..addresses.countries import COUNTRIES
from ..licenses.models import License
from ..specialties.models import SpecialtyCode
from ..direct.models import DirectAddress, DirectCertificate
from ..identifiers.models import Identifier
from localflavor.us.models import PhoneNumberField
from django.db import transaction
from slugify import slugify
from django_extensions.db.fields import UUIDField
from baluhn import generate, verify

ENUMERATION_TYPE_CHOICES = (("NPI-1","Individual National Provider Identifier (NPI-1)"),
                            ("NPI-2","Organizational National Provider Identifier (NPI-2)"),
                            ("HPID","Health Plan Identifier (HPID)"),
                            ("OEID","Other Entity Individual Atypical Provider (OEID)"),)


ENUMERATION_MODE_CHOICES = (("W", "Web"),("P", "Paper"), ("E","EFI"), ("C","CSV"))

ENUMERATION_STATUS_CHOICES  = (("E", "Editing"),  ("P", "Pending"), ("A", "Active"),
                               ("D", "Deactived"), ("R","Rejected"),)

DECACTIVAED_REASON_CHOICES = (("", "Blank"), ("DT", "Death"), ("DB", "Business Dissolved"),
                                ("FR", "Fraud"), ("OT", "Other"), )

ENTITY_CHOICES = (("INDIVIDUAL", "Individual"), ("ORGANIZATION", "Organization"))


INDIVIDUAL_OTHER_NAME_CHOICES = (("","Blank"), ("1","Former Name"),
                                ("2","Professional Name"),
                                ("5","Other Name"))

ORGANIZATION_OTHER_NAME_CHOICES = (("","Blank"), ("3","Doing Business As"),
                ("4","Former Legal Business Name"), ("5","Other Name"))


GENDER_CHOICES = (("F","Female"), ("M","Male"), ("T","Transgender"))

PREFIX_CHOICES = (('Ms.', 'Ms.'),('Mr.', 'Mr.'),('Miss','Miss'),
                  ('Mrs.','Mrs.'),('Dr.','Dr.'),('Prof.','Prof.'))


SUFFIX_CHOICES = (('Jr.','Jr.'),('Sr.','Sr.'),('I','I'),('II','II'),
                  ('III','III'),('IV','IV'),('V','V'),('VI','VI'),
                  ('VII','VII'),('VIII','VIII'),('IX','IX'),('X','X'),)

SOLE_PROPRIETOR_CHOICES = (("", "No Answer"), ("YES", "Yes"),("NO", "No"))

def generateUUID():
    return str(uuid.uuid4())

class Enumeration(models.Model):
    
    
    status              = models.CharField(max_length=1,
                                    choices=ENUMERATION_STATUS_CHOICES,
                                    default ="E", blank=True)
    
    mode                = models.CharField(max_length=1,
                                    choices=ENUMERATION_MODE_CHOICES,
                                    default ="W",
                                    verbose_name="Mode of Enumeration")
    
    enumeration_type    = models.CharField(max_length=5,
                                    choices=ENUMERATION_TYPE_CHOICES,)
        
    number              = models.CharField(max_length=10, blank=True, default="",
                            #editable=False,
                            db_index=True)
    
    old_numbers         = models.CharField(max_length=50, blank=True, default="",
                            #editable=False,
                            help_text="Old NPIs in case of a replacement number.")
    
    is_number_replaced  = models.BooleanField(default=False, editable=True)


    is_reactivated      = models.BooleanField(default=False, editable=True)
    
    has_ever_been_active   = models.BooleanField(default=False, editable=True)
    has_ever_been_deactive = models.BooleanField(default=False, editable=True)
    flag_for_deactivation  = models.BooleanField(default=False,
                            help_text="Check this box to flag this record for enumeration. Final deactivation processed by CMS.")
    decativation_note       = models.TextField(max_length=1024, blank=True,
                                default="",
                                help_text="Why do you wish to deactive this record?")
    pii_lock               = models.BooleanField(default=False,
                                help_text="If False, then DOB, SSN, and ITIN can be changed.")
    #Gatekeeper fields
    practice_address_error     = models.BooleanField(default=False, editable=True)
    mailing_address_error      = models.BooleanField(default=False, editable=True)
    invalid_ssn_error          = models.BooleanField(default=False, editable=True)
    invalid_ein_error          = models.BooleanField(default=False, editable=True)
    ssn_already_issued_error   = models.BooleanField(default=False, editable=True)
    lst_error                  = models.BooleanField(default=False, editable=True)
    confirmation               = models.BooleanField(default=False,
                                    help_text =
                                    """I understand that the infomation on this site,
                                    except for personally identifiable information such
                                    as SSN, EIN, ITIN, date of birth, and place of
                                    birth IS MADE PUBLIC in accordance with US
                                    federal regulations. """)
    #end Gatekeeper fields


    tracking            = UUIDField(db_index=True)
    
    handle              = models.SlugField(unique=True, default=generateUUID)
    
    enumeration_date    = models.DateField(blank=True, null=True, db_index=True)
    
    flag_for_fraud      = models.BooleanField(default=False)
    fraud_alert_note    = models.TextField(max_length=1024, blank=True,
                                default="",
                                help_text="Please explain the alleged or suspected fraud associaed with this record.")
    
    
    has_ever_been_fraud_alert  = models.BooleanField(default=False)
    
    name_prefix         = models.CharField(choices=PREFIX_CHOICES, max_length=5,
                                blank=True, default="")
    
    first_name          = models.CharField(max_length=150, blank=True,
                                default="", db_index=True)
    
    middle_name               = models.CharField(max_length=150, blank=True,
                                                 default="")
    
    last_name                 = models.CharField(max_length=150, blank=True,
                                                   default="", db_index=True)
    
    name_suffix               = models.CharField(choices=SUFFIX_CHOICES, max_length=4,
                                           blank=True, default="")

    
    sole_proprietor           = models.CharField(choices = SOLE_PROPRIETOR_CHOICES,
                                               blank=True, default="", max_length=3)
    organizational_subpart    = models.BooleanField(default=False)
    
    credential                = models.CharField(max_length=50, blank=True,
                                    default="", help_text ="e.g. MD, PA, OBGYN, DO")
    
    organization_name         = models.CharField(max_length=300, blank=True,
                                    default="", db_index=True,
                                    verbose_name="Legal Business Name")
    
    doing_business_as         = models.CharField(max_length=300, blank=True,
                                                 default="")
     
    organization_other_name   = models.CharField(max_length=300, blank=True,
                                                 default="")
    
    organization_other_name_code  = models.CharField(max_length=1, blank=True,
                                                     default="",
                                    choices=ORGANIZATION_OTHER_NAME_CHOICES)
    
    other_first_name_1      = models.CharField(max_length=100, blank=True,
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
    gravatar_email             = models.EmailField(max_length=200,   blank=True, default="",
                                    help_text="Add an avatar image to your public profile by provding an email registered with Gravatar.com. This email will not be public.")
    facebook_handle            = models.CharField(max_length=100,   blank=True, default="")
    twitter_handle             = models.CharField(max_length=100,   blank=True, default="")
    public_email               = models.EmailField(blank=True,      default="")
    
    
    driving_directions         = models.TextField(max_length=256,   blank=True, default="")
    bio_headline               = models.CharField(max_length=255,   blank=True, default="")
   
    background_image           = models.ImageField(blank = True,    null=False, default='',
                                    max_length=255L, upload_to="enumeration-backgrounds",
                                    verbose_name= "Background Image")
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
    
    specialty                   = models.ForeignKey(SpecialtyCode, null=True, blank=True,
                                        related_name ="enumeration_primary_specialty",
                                        verbose_name="Primary Specialty",
                                        db_index=True)
    
    
    specialties                 = models.ManyToManyField(SpecialtyCode, null=True, blank=True,
                                        related_name = "enumerations_specialties",
                                        db_index=True)
    
    direct_addresses            = models.ManyToManyField(DirectAddress, null=True, blank=True,
                                        related_name = "enumerations_direct_addresses",
                                        db_index=True)
    
    direct_certificates         = models.ManyToManyField(DirectCertificate, null=True, blank=True,
                                        related_name = "enumerations_direct_certificates",
                                        db_index=True)
    
    
    managers                    = models.ManyToManyField(User, null=True,
                                            blank=True, db_index=True,
                                            related_name ="enumeration_managers"
                                            )
    

    #PII --------------------------------------------------------------------
    state_of_birth      = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATE_W_FC_CHOICES,
                        help_text="""Choose "Foreign Country" at the bottom of the list if the individual was not born in the US.""")
    
    country_of_birth    = models.CharField(max_length=2,  blank=True, default="US",
                                    choices = COUNTRIES)
    
    date_of_birth          = models.DateField(blank=True, null=True,
                                           help_text="Format: YYYY-MM-DD")
    
    gender      = models.CharField(max_length=2,  blank=True, default="",
                        verbose_name = "Sex", choices = GENDER_CHOICES )
    
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
    
    contact_person_telephone_number     = PhoneNumberField(max_length=12,
                                            blank=True, default="",
                                            help_text="Format: XXX-XXX-XXXX.")
    contact_person_telephone_extension   = models.CharField(max_length=10,
                                                  blank=True, default="")
    contact_person_title_or_position     = models.CharField(max_length=150,
                                                  blank=True, default="")

    contact_person_title = models.CharField(max_length=150, blank=True,
                                            default="")
    
    authorized_official_email = models.EmailField(blank=True, default="",
                               help_text = "Required if the authorized official has an email.",
                               db_index=True)
    
    # End PII -----------------------------------------------------------------
    authorized_official_prefix        = models.CharField(choices=PREFIX_CHOICES, max_length=10,
                                            blank=True, default="")
    
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
    
    comments            = models.TextField(blank=True, default="", max_length=1024)
    last_updated        = models.DateField(blank=True, null=True)
    added               = models.DateField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    enumerated_by       = models.ForeignKey(User, blank=True, null=True, editable=False)
    last_updated_ip     = models.CharField(max_length=20, blank=True,
                                default="", db_index=True)
    
    
    
    class Meta:
        get_latest_by = "id"
        ordering = ('-enumeration_date',)


    def name(self):
        name = "Not Provided"
        if self.enumeration_type in ("HPID", "OEID", "NPI-2"):
            name = self.organization_name.capitalize()
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as,
                                    self.organization_name.capitalize())
        elif self.enumeration_type in ("NPI-1", ):
            name = "%s %s" % (self.first_name.capitalize(),
                              self.last_name.capitalize())
            if self.doing_business_as:
                name = "%s %s (%s)" % (self.first_name.capitalize(),
                                       self.last_name.capitalize(),
                                       self.doing_business_as.capitalize(),)

        if not name or name== " ":
            return "Not Provided"
        return name

    def pretty_status(self):
        ps = "Could generate pretty status"
        
        if self.status=="A":
            ps = "%s. Enumerated on %s. Updated on %s" % (self.get_status_display(),
                                            self.enumeration_date, self.last_updated)
        if self.status=="D":
            ps = "%s. Deactivated on %s." % (self.get_status_display(),
                                            self.deactivation_date)
        if self.status in ("P", "R"):
            ps = "%s. Updated on %s." % (self.get_status_display(),
                                            self.last_updated)
        return ps

    def entity_type(self):
        entity_type = None
        if self.enumeration_type in ("HPID", "OEID", "NPI-2"):
            entity_type = "Organization"
        elif self.enumeration_type in ("NPI-1",):
            entity_type = "Individual"
        return entity_type
    

    def entity_type_formal(self):
        entity_type = None
        if self.enumeration_type in ("HPID", "OEID", "NPI-2"):
            entity_type = "Entity Type 2"
        elif self.enumeration_type in ("NPI-1",):
            entity_type = "Entity Type 1"
        return entity_type

    
    def secure_gravatar_url(self):
        import urllib, hashlib
        default = "mm"
        size   = 140
        gravatar_url = "https://www.gravatar.com/avatar/" + \
                       hashlib.md5(self.gravatar_email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size), 'r':'g'})
        return gravatar_url
    
    def pretty_number(self):
        if not self.number:
            return  "Unassigned"
           
        return self.number
    
    def google_map_q(self):
        
        address_plus = str(self.location_address).replace(" ", "+")
        return address_plus
    


    def detail(self):
        name = "Not Provided"
        if self.enumeration_type in ("HPID", "NPI-2"):
            name = self.organization_name
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as,
                                    self.organization_name)
        elif self.enumeration_type in ("OEID", "NPI-1"):
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
            name = "Not Provided"
        
        e = "%s %s is an %s managed by %s." % (number, name,
                                               self.enumeration_type, managers)
        return e

    def verify_luhn(self):
        prefixed_number = "%s%s" % (settings.LUHN_PREFIX, self.number)
        return verify(prefixed_number)            
        


    def gatekeeper(self):
        msglist = []
        
        if Enumeration.objects.filter(ssn=self.ssn).count() > 1:
            self.ssn_already_issued_error = True
            msg = "There is an issue with your SSN. Please contact the help desk."
            msglist.append(msg)
            
        if self.enumeration_type in ("OEID", "NPI-1") and not self.ssn and not self.itin:
            msg = "No SSN or ITIN supplied."
            msglist.append(msg)
 
        if self.enumeration_type in ("OEID", "NPI-1") and not self.date_of_birth:
            msg = "No date of birth supplied."
            msglist.append(msg)
            
        
        if self.enumeration_type in ("HPID", "NPI-2") and not self.ein:
            msg = "No EIN supplied."
            msglist.append(msg)
            
        if self.invalid_ssn_error:
            msg = "Your SSN could not be verified."
            msglist.append(msg)
        
        if self.practice_address_error:
            msg = "Your practice address did not validate."
            msglist.append(msg)
            
        if self.mailing_address_error:
            msg = "Your mailing address did not validate."
            msglist.append(msg)
            
        if self.lst_error:
            msg = "There was an issue with your taxonomy and license combination."
            msglist.append(msg)
        
        return msglist

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




    
    
    
    def save(self, commit=True, **kwargs):
    
        """Set Sole Proprieter to NO if its an organization"""
        if self.enumeration_type in ("HPID", "OEID", "NPI-2"):
            self.sole_proprietor="NO"
        
        
        """Mark the has ever been marked for fraud flag if fraud_alert==True"""
        if self.flag_for_fraud:
            self.has_ever_been_fraud_alert=True
        
        """Mark the has ever been active flag if the record is active"""        
        if self.status=="A":
            self.deactivation_date=None
            self.has_ever_been_active=True
            
        """Mark the has ever been deactive flag if the record is deactive"""     
        if self.status=="D":
            self.has_ever_been_deactive=True
            if not self.deactivation_date:
                self.deactivation_date = date.today()
            
        """Mark the is_number_replaced flag if old numbers exist."""        
        if self.old_numbers:
            self.is_number_replaced=True
        
        """Create a name for the handle """
        name = self.handle #Make it a UUID for starters to ensure unique
    
        #Now try and set it something more sensible
        if self.enumeration_type in ("HPID", "OEID", "NPI-2") and self.organization_name:
            name = self.organization_name
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as,
                                    self.organization_name)
        elif self.enumeration_type in ("NPI-1", ) and self.first_name and self.last_name:
            name = "%s %s" % (self.first_name, self.last_name)
            if self.doing_business_as:
                name = "%s %s (%s)" % (self.first_name,
                                       self.last_name,
                                       self.doing_business_as,)
        
        
        """Slugify the handle if not already created"""        
        if valid_uuid(self.handle) and not valid_uuid(name):
            slug_handle = slugify(name)
        else:
            slug_handle = slugify(self.handle)
        #If the handle is taken, set it to something else.
        if Enumeration.objects.filter(handle=slug_handle).exclude(handle=self.handle).count()==0:
            self.handle = slug_handle
        else:    
            self.handle = "%s%s" % (slug_handle, random.randrange(10000,99999))
            
                
        """Set the Doing business AS if organization_other_name_code=="3" and
        the field was left blank."""
        if self.organization_other_name and self.organization_other_name_code=="3" and \
           not self.doing_business_as:
            self.doing_business_as = self.organization_other_name
        
        
        """If the status is active but no enumeration number is assigned then create one."""
        if self.status == "A" and self.number == "":
            if self.enumeration_type in ("NPI-1", "NPI-2"):
                
                if settings.VERIFY_LUHN_AND_UNIQUE_ENUMERATION:
                    #create a candidate eumeration
                    eight_digits = random.randrange(10000000,19999999)
                    
                    prefixed_eight_digits = "%s%s" % (settings.LUHN_PREFIX, eight_digits)
                    
                    checkdigit = generate(prefixed_eight_digits)
                    
                    self.number = "%s%s" % (eight_digits, checkdigit)
                    while Enumeration.objects.filter(number=self.number).count()>0:
                        eight_digits = random.randrange(10000000,19999999)
                        prefixed_eight_digits = "%s%s" % (settings.LUHN_PREFIX, eight_digits)
                        checkdigit = generate(prefixed_eight_digits)
                        self.number = "%s%s" % (eight_digits, checkdigit)
                else:
                    self.number = random.randrange(100000000,199999999)
                    
            
                
            
            if self.enumeration_type in ("HPID"):
                self.number = random.randrange(7000000000,7999999999)
             
            if self.enumeration_type in ("OEID", "OEID"):
                self.number = random.randrange(6000000000,6999999999)
            self.enumeration_date = date.today()
         
        if self.status == "R":
            self.enumeration_date = date.today()
            
        
        """Captialize all names"""
        self.first_name =self.first_name.upper()
        self.middle_name =self.middle_name.upper()
        self.last_name =self.last_name.upper()
        self.authorized_official_first_name  = self.authorized_official_first_name.upper()    
        self.authorized_official_middle_name = self.authorized_official_middle_name.upper() 
        self.authorized_official_last_name   = self.authorized_official_last_name.upper()
        self.contact_person_first_name  = self.contact_person_first_name.upper()   
        self.contact_person_middle_name = self.contact_person_middle_name.upper()
        self.contact_person_last_name   = self.contact_person_last_name.upper()

        
        
        
        """Default the IP address if it cannot be determined"""
        if not self.last_updated_ip:
            self.last_updated_ip = "127.0.0.1"
        
        """Set last updated date unless exlicitly suppressed."""
        if settings.UPDATE_LAST_UPDATE_DATE:
            self.last_updated = date.today()
                
        if commit:
            
            super(Enumeration, self).save(**kwargs)
        
