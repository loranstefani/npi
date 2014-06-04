from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage,  EmailMultiAlternatives
from datetime import date
from ..taxonomy.models import TaxonomyCode
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
import uuid, random, datetime, json
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


EVENT_CHOICES = ( ('ADVERSE-EVENT','Adverse Event'),
                  ('FINAL-ACTION','Final Action'),
                  ('ACTIVATION','Activation'),
                  ('REJECTION','Rejection'),
                  ('FUZZY-DECEASED','Fuzzy Deceased'),
                  ('DEACTIVATED-DECEASED','De-activation Deceased'),
                  ("DEACTIVATED-BUSINESS_DISOLVED", "De-activation Business Dissolved"),
                  ("DEACTIVATED_FRAUD", "De-activation Fraud"),
                  ("DEACTIVATED_OTHER", "De-activation Other"),
                  ('REACTIVATION','Re-activation'),
                  ('REENUMERATION','Reenumeration'),
                  ('NAME-CHANGE','Name Change'),
                  ('SSN-CHANGE','SSN Change'),
                  )


CONTACT_METHOD_CHOICES = (("E","Email"),("M","Mail"))

ERROR_CHOICES = ( ('ADDRESS','Address'),
                  ('SSN-ALREADY-ASSIGNED','Another record with SSN was assigned'),
                  ('SSN-INVALID','SSN Invalid'),
                  ('LICENSE','License Problem'),
                  ('TAXONOMY','Taxonomy'),
                  ('LICENSE-TAXONOMY','License/Taxonomy Mismatch'),
                  ('FIELD','A field did not validate.'),
                  )

ENUMERATION_MODE_CHOICES = (("W", "Web"),("P", "Paper"), ("E","EFI"), ("C","CSV"))

ENUMERATION_CLASSIFICATION_CHOICES = (("N", "New"),("C", "Change Request"))

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
    
    classification                = models.CharField(max_length=1,
                                    choices=ENUMERATION_CLASSIFICATION_CHOICES,
                                    default ="N",)
    
    
    enumeration_type    = models.CharField(max_length=5,
                                    choices=ENUMERATION_TYPE_CHOICES,)
    
    contact_method         = models.CharField(max_length=1,
                                    choices=CONTACT_METHOD_CHOICES,
                                    default="E", blank=True)
        
    number               = models.CharField(max_length=10, blank=True, default="",
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
                            help_text="Check this box to flag this record for deactivation. Final deactivation processed by CMS.")
    decativation_note       = models.TextField(max_length=1024, blank=True,
                                default="",
                                help_text="Why do you wish to deactivate this record?")
    
    flag_for_reactivation  = models.BooleanField(default=False,
                            help_text="Check this box to flag this record for reactivation. Final deactivation processed by CMS.")
    recativation_note       = models.TextField(max_length=1024, blank=True,
                                default="",
                                help_text="Why do you wish to reactivate this record?")


    pii_lock               = models.BooleanField(default=False,
                                help_text="If False, then DOB, SSN, and ITIN can be changed.")
    confirmation               = models.BooleanField(default=False,
                                    help_text =
                                    """I understand that the infomation on this site,
                                    except for personally identifiable information such
                                    as SSN, EIN, ITIN, date of birth, and place of
                                    birth IS MADE PUBLIC in accordance with US
                                    federal regulations. """)



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
                                default="", help_text="Previous or Maiden Last Name") 

    other_name_prefix_1     = models.CharField(choices=PREFIX_CHOICES, max_length=5,
                                    blank=True, default="")
    
    other_name_suffix_1     = models.CharField(choices=SUFFIX_CHOICES, max_length=4, blank=True,
                                                   default="")

    other_name_credential_1  = models.CharField(max_length=20, blank=True, default="")

    other_name_code_1  = models.CharField(max_length=1, blank=True, default="",
                                    choices=INDIVIDUAL_OTHER_NAME_CHOICES)
    other_first_name_2    = models.CharField(max_length=100, blank=True,
                                       default="",
                                       help_text="Another previous first name")

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
    
    date_of_death          = models.DateField(blank=True, null=True,
                                   help_text="Format: YYYY-MM-DD")
    
    gender      = models.CharField(max_length=2,  blank=True, default="",
                        verbose_name = "Sex", choices = GENDER_CHOICES )
    
    itin        = models.CharField(max_length=10, blank=True,
                        default="", verbose_name="IRS Individual Tax Payer Identification Number (ITIN)",
                        help_text = "An ITIN is required for individuals that are not eligible for a social security number (SSN).",
                        db_index=True)
    
    itin_image   = models.ImageField(blank = True, null=False, default='',
                    max_length=255L, upload_to="itin-verification",
                    verbose_name= "ITIN Image",
                    help_text ="If you have an ITIN, please upload an image of one form of identification or proof in PDF, PNG, JPG, or BMP format.",)
    
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
    
    #End PII/Sensitive
    
    # Death Information (When Appliciable) ------------------------------
    deceased_in_dmf             = models.BooleanField(blank=True, default=False)
    deceased_fuzzy_match        = models.BooleanField(blank=True, default=False,
                                    help_text = "True when SSN matches but name DOB does not.")
    deceased_notice_day_sent    = models.DateField(blank=True, null=True,
                                           help_text="Format: YYYY-MM-DD")
    deceased_notes              = models.TextField(max_length=1000, blank=True, default="")
    dmf_incorrect               = models.BooleanField(blank=True, default=False,
                                    help_text = "DMF appears to be incorrect. Individual is not actually deceased.")
    
    # Deactivation information ---------------------------
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
    initial_enumeration_date = models.DateField(blank=True, null=True)
    
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
    

    def get_absolute_url(self):
        return reverse('display_enumeration_profile', args=[str(self.number)])



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

    def luhn_verify(self):
        prefixed_number = "%s%s" % (settings.LUHN_PREFIX, self.number)
        return verify(prefixed_number)            
        
    def ssn_verify(self):
        
        """Add SSN validation code here."""
        """Return True for valid and False for invalid"""
        return True
        
    def ein_verify(self):
        
        """Add EIN validation code here."""
        """Return True for valid and False for invalid"""
        return True    

    def license_taxonomy_verify(self):
        
        """Add License/Taxonomy validation code here."""
        """Return True for valid and False for invalid"""
        return True  
        
    def gatekeeper(self):
        """Return a list of errors or an empty list"""

        #create an empty message list
        msglist = []
        
        if not settings.GATEKEEPER:
            #The gatekeeper has be deactivated so return an empty list of errors.
            return msglist
        
        # Get all the errors and delete them
        g = GateKeeperError.objects.filter(enumeration=self)
        g.delete()
        
        
        #create an empty message list ------------------------------------------
        
        if Enumeration.objects.filter(ssn=self.ssn).count() > 1:
            e =GateKeeperError.objects.create(
                enumeration =self,
                error_type="SSN-ALREADY-ASSIGNED",
                error_critical = True,
                note= "There is an issue with your SSN. Please contact the help desk.")
            msglist.append(e)
            
        if self.enumeration_type in ("OEID", "NPI-1") and not self.ssn and not self.itin:
            e =GateKeeperError.objects.create(
                    enumeration =self,
                    critical_error = True,
                    error_type="SSN-INVALID",
                    note= "No SSN or ITIN supplied.")
            msglist.append(e)
            
        #Check some things for individuals
        if self.enumeration_type in ("OEID", "NPI-1"):
            
            #If not DOB
            if not self.date_of_birth:
                e =GateKeeperError.objects.create(
                    enumeration =self,
                    critical_error = True,
                    error_type="FIELD",
                    note= "No date of birth supplied.")
                msglist.append(e)
            
            
            #If no name
            if not self.first_name:
                e =GateKeeperError.objects.create(
                    enumeration =self,
                    critical_error = True,
                    error_type="FIELD",
                    note= "No first name was supplied.")
                msglist.append(e)
                
                
            if not self.last_name:
                e =GateKeeperError.objects.create(
                    enumeration =self,
                    critical_error = True,
                    error_type="FIELD",
                    note= "No last name was supplied.")
                msglist.append(e)
      
                  
            if not self.ssn_verify():
                e = GateKeeperError.objects.create(
                    enumeration =self,
                    critical_error = True,
                    error_type="SSN-INVALID",
                    note= "The SSN could not be verified.")
                msglist.append(e)
            
        if self.enumeration_type in ("HPID", "NPI-2"):
            if not self.ein:
                e =GateKeeperError.objects.create(
                    enumeration =self,
                    error_type="FIELD",
                    critical_error = True,
                    note= "No EIN was supplied.")
                msglist.append(e)
            
            if not self.organization_name:
                e =GateKeeperError.objects.create(
                    enumeration =self,
                    error_type="FIELD",
                    critical_error = True,
                    note= "No organization name supplied.")
                msglist.append(e)
                
        
        if not self.contact_person_first_name or not self.contact_person_last_name:
            e =GateKeeperError.objects.create(
                    enumeration =self,
                    error_type="FIELD",
                    note= "No contact person was supplied.")
            msglist.append(e)
            
    
    
    
        if not self.mailing_address:
            e =GateKeeperError.objects.create(
                    enumeration =self,
                    error_type="ADDRESS",
                    critical_error = True,
                    note= "No mailing address was supplied.")
            msglist.append(e)
        
        else:
            #there is an address but does it validate?
            if not self.mailing_address.verify():
                e =GateKeeperError.objects.create(
                    enumeration =self,
                    error_type="ADDRESS",
                    note= "The mailing address could not be verified.")
                msglist.append(e)
            
        if not self.location_address:
            e =GateKeeperError.objects.create(
                    enumeration =self,
                    error_type="ADDRESS",
                    critical_error = True,
                    note= "No practice location address was supplied.")
            msglist.append(e)
        else:
            #there is an address but does it validate?
            if not self.location_address.verify():
                e =GateKeeperError.objects.create(
                    enumeration =self,
                    error_type="ADDRESS",
                    note= "The practice location address could not be verified.")
                msglist.append(e)
            

        if not self.taxonomy:
            e =GateKeeperError.objects.create(
                    enumeration =self,
                    error_type="TAXONOMY",
                    critical_error = True,
                    note= "No primary taxonomy was provided.")
            msglist.append(e) 
    
        self.save()
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
            
        e = "%s (%s) %s" % (name, self.enumeration_type, number)
        return e




    
    
    
    def save(self, commit=True, **kwargs):
    
        """Set Sole Proprieter to NO if its an organization"""
        if self.enumeration_type in ("HPID", "OEID", "NPI-2"):
            self.sole_proprietor = "NO"
        
        
        """Mark the has ever been marked for fraud flag if fraud_alert==True"""
        if self.flag_for_fraud:
            self.has_ever_been_fraud_alert = True
        
        "If the record has ever been active make it as a change (not new)"
        if self.has_ever_been_active == True:
            self.classification = "C"
        
        
        """If Active. Mark the has ever been active flag if the record is active"""        
        if self.status == "A":
            self.deactivation_date = None
            self.has_ever_been_active = True
            #Remove all gatekeeper errors.
            GateKeeperError.objects.filter(enumeration=self).delete()
        
            
        """Mark the has ever been deactive flag if the record is deactive"""     
        if self.status == "D":
            self.has_ever_been_deactive = True
            if not self.deactivation_date:
                self.deactivation_date = date.today()
        
        """If the record is rejected"""
        if self.status == "R":
            self.enumeration_date = None
            
        """If the record has been edited."""    
        if self.status in ("E", "A") :
            self.last_updated = date.today()
            
           
        """Mark the is_number_replaced flag if old numbers exist."""        
        if self.old_numbers:
            self.is_number_replaced = True
        
        
        """If the status is active but no enumeration number is assigned then create one."""
        if self.status == "A" and self.number == "":
            """This is new so mark it as such"""
            self.classification = "N"
            
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
                    
            
                
            #Create and HPID
            if self.enumeration_type == "HPID":
                self.number = random.randrange(7000000000,7999999999)
             
            #C
            if self.enumeration_type == "OEID":
                self.number = random.randrange(6000000000,6999999999)
            
            self.initial_enumeration_date = date.today()
            self.enumeration_date = date.today()


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

        """Captialize all names"""
        self.first_name                      = self.first_name.upper()
        self.middle_name                     = self.middle_name.upper()
        self.last_name                       = self.last_name.upper()
        self.authorized_official_first_name  = self.authorized_official_first_name.upper()    
        self.authorized_official_middle_name = self.authorized_official_middle_name.upper() 
        self.authorized_official_last_name   = self.authorized_official_last_name.upper()
        self.contact_person_first_name       = self.contact_person_first_name.upper()   
        self.contact_person_middle_name      = self.contact_person_middle_name.upper()
        self.contact_person_last_name        = self.contact_person_last_name.upper()

        
        
        
        """Default the IP address if it cannot be determined"""
        if not self.last_updated_ip:
            self.last_updated_ip = "127.0.0.1"
        
        """Set last updated date unless exlicitly suppressed."""
        if settings.UPDATE_LAST_UPDATE_DATE:
            self.last_updated = date.today()
        
        
        """Reset the confirmation flag"""
        self.confirmation= False
              
        if commit:
            
            super(Enumeration, self).save(**kwargs)
        





class Event(models.Model):
    enumeration = models.ForeignKey(Enumeration, db_index=True)
    event_type  = models.CharField(choices = EVENT_CHOICES, max_length=20,
                                   db_index=True)
    subject     = models.CharField(max_length=200, default="", blank=True)
    
    body        = models.TextField(max_length=2048, default="", blank=True)
    
    details       = models.TextField(max_length=2048, default="", blank=True)
    
    notify_contact_person   = models.BooleanField(default=False, blank=True,
                                help_text= "If checked, the contact person will receive a notification.")
    
    send_now   = models.BooleanField(default=True, blank=True,
                        help_text= "If checked, the notification will be sent/resent to contact person via the default contact method.")
    
    
    send_mail_now   = models.BooleanField(default=False, blank=True,
                        help_text= "If checked, the notification will be sent/resent to contact person by mail.")
        
    send_email_now   = models.BooleanField(default=False, blank=True,
                        help_text= "If checked, the notification will be sent/resent to contact person by email.")
    
    notification_sent       = models.BooleanField(default=False, blank=True,
                        help_text= "Notification Sent")
    
    email_sent          = models.BooleanField(default=False, blank=True)
    mail_sent           = models.BooleanField(default=False, blank=True)
    
    note                    = models.TextField(max_length=1024, blank=True, default="")
    
    added                   = models.DateField()#auto_now_add=True
    
    updated                 = models.DateField(auto_now=True)
    


    class Meta:
        get_latest_by = "id"
        ordering = ('-updated', '-added')
        
    def __unicode__(self):
        return "%s %s %s" % (self.enumeration, self.event_type, self.added)
    
    
    def as_json(self):
        d = {"enumeration_number": self.enumeration.number,
            "enumeration_type": self.enumeration.enumeration_type,
            "enumeration_name": self.enumeration.name(),
            "event_type": self.event_type,          
            "status" : self.status,
            "subject" : self.subject,
            "body" : self.body,
            "details" : self.details,
            "notify_contact_person": self.notify_contact_person, 
            "send_now": self.send_now,
            "notification_sent": self.notification_sent,
            "mail_sent": self.mail_sent,
            "email_sent": self.email_sent,  
            "note": self.note,                   
            "added": str(self.added),                  
            "updated":str(self.updated)               
             }
        return json.dumps(d, indent=4)
        

    def as_dict(self):
        d = {"enumeration_number": self.enumeration.number,
            "enumeration_type": self.enumeration.enumeration_type,
            "enumeration_name": self.enumeration.name(),
            "event_type": self.event_type,          
            "status" : self.status,
            "subject" : self.subject,
            "body" : self.body,
            "details" : self.details,
            "notify_contact_person": self.notify_contact_person, 
            "send_now": self.send_now,
            "notification_sent": self.notification_sent,
            "mail_sent": self.mail_sent,
            "email_sent": self.email_sent,  
            "note": self.note,                   
            "added": str(self.added),                  
            "updated":str(self.updated)               
             }
        return d
        

    def send_event_notification_mail(self):
        sent = False
        #Add code here to generate PDF and mail labels.
        out = "Send a mail to %s %s @ %s" % (self.enumeration.contact_person_first_name,
                                             self.enumeration.contact_person_last_name,
                                             self.enumeration.mailing_address)
        print out
        sent = True
        return sent
        


    def send_event_notification_email(self):
        """Send notice by Email"""
        sent = False
        if self.enumeration.contact_person_email and self.enumeration.contact_method =="E":
            """If an email address exists, then send it."""            
            subject = "[%s] %s" % (settings.ORGANIZATION_NAME,self.subject)    
            from_email = settings.EMAIL_HOST_USER
            to = self.enumeration.contact_person_email 
            headers = {'Reply-To': from_email}
            
            html_content = """
            Hello %s %s
            
            <p>
            %s
            </p>
            <h1>Details</h1>
            <p>
            %s
            </p>
            <p>
            <p>
            Sincerely,
            </p>
            The NPPES Team @ CMS
            </p>
            """ % (self.enumeration.contact_person_first_name,
                   self.enumeration.contact_person_last_name,
                   self.body, self.details)
           
            text_content="""Hello: %s %s,
                %s
                Details
                =======
                %s
                
                Sincerely,
                
                The NPPES Team @ CMS
                
            """ % (self.enumeration.contact_person_first_name,
                   self.enumeration.contact_person_last_name,
                   self.body, self.details)
            msg = EmailMultiAlternatives(subject, text_content, from_email,
                                         [to,settings.INVITE_REQUEST_ADMIN, ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            sent = True
            
        return sent


    
    def save(self, commit=True, **kwargs):
        
        if self.send_now or (self.notification_sent==False and \
                             self.notify_contact_person==True):
            #Send notification
            
            if self.enumeration.contact_method == "E":    
                if self.send_event_notification_email()== True:
                    #Flag message as sent.
                    self.notification_sent =True
                    self.email_sent = True
            
            elif self.enumeration.contact_method == "M":
                if self.send_event_notification_mail() == True:
                    #Flag message as sent.
                    self.notification_sent =True
                    self.mail_sent = True
                
        #force an email    
        if self.send_email_now:
            if self.send_event_notification_email()== True:
                #Flag message as sent.
                self.notification_sent =True
                self.email_sent = True
            
        #force a mail 
        if self.send_mail_now:
            if self.send_event_notification_mail() == True:
                #Flag message as sent.
                self.notification_sent =True
                self.mail_sent = True
                
        
            #Reset our send now flags.
            self.send_now       = False
            self.send_email_now = False
            self.send_mail_now  = False
        
        if not self.added:
            self.added= datetime.date.today()
        super(Event, self).save(**kwargs)


class GateKeeperError(models.Model):
    enumeration = models.ForeignKey(Enumeration, db_index=True)
    error_type  = models.CharField(choices = ERROR_CHOICES,
                                   max_length=20,
                                   db_index=True)
    
    critical_error  = models.BooleanField(default=False, blank=True,
                        help_text= "If checked, the Enumeration cannot be submitted for enumeration.")
    
    added       = models.DateField(auto_now_add=True,
                                   db_index=True,)
    
    note        = models.TextField(max_length=1024, blank=True,
                                   default="", null=True)
    def __unicode__(self):
        return "%s %s %s" % (self.enumeration, self.error_type, self.added)
        
    def save(self, commit=True, **kwargs):
        if not self.added:
            self.added= datetime.date.today()
        super(GateKeeperError, self).save(**kwargs)
    