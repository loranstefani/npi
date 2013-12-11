from django.db import models
from django.conf import settings
from ..taxonomy.models import TaxonomyCode
from django.contrib.auth.models import User
import uuid
from localflavor.us.us_states import US_STATES

US_STATE_CHOICES = list(US_STATES)
US_STATE_CHOICES.insert(0, ('', 'Please Choose a State'))
US_STATE_CHOICES.append(('ZZ', 'Foreign Country'))



ENUMERATION_TYPE_CHOICES = (("NPI-1","Individual Provider (NPI-1)"),
                       ("NPI-2","Provider Organization (NPI-2)"),
                       ("HPID","Health Plan Identifier (HPID)"),
                        ("OEID-1","Individual Atypical Provider (OEID-1)"),
                        ("OEID-2","Atypical Provider Organization (OEID-2)"),
                        )
ENUMERATION_STATUS_CHOICES  = (("P", "Pending"), ("A", "Active"), ("D", "Deactived"), )
DECACTIVAED_REASON_CHOICES = (("", "Blank"), ("D", "Deceased"), ("F", "Fraud"), ("O", "Other"), )
ADDRESS_TYPE_CHOICES    = (("PRACTICE-DOM", "Practice Address (Domestic)"),
                           ("BUSINESS-DOM", "Business/Billing Address (Domestic)"),
                           
                           ("PRACTICE-FOR", "Practice Address (Foreign)"),
                           ("BUSINESS-FOR", "Business/Billing Address (Foreign)"),

                           ("PRACTICE-MIL", "Practice Address (Military)"),
                           ("BUSINESS-MIL", "Business/Billing Address (Military)"),
                        )
ENTITY_CHOICES = (("INDIVIDUAL", "Individual"), ("ORGANIZATION", "Organization"))

COUNTRY_CHOICES = (("US", "United States"), ("CA", "Canada"), ("MX", "Mexico"))

LICENSE_STATUS_CHOICES =(("UNK", "Unknown"),("ACTIVE","Active"),
                         ("ACTIVE_WITH_RESTRICTIONS","Active with Restrictions"),
                         ("EXPIRED","Expired"),
                         ("REVOKED","Revoked"),
                         ("DECEASED","Deceased"),
                         )

LICENSE_TYPE_CHOICES =(  ("MD", "Medical Doctor (MD)"),
                          ("DO","Doctor of Osteopathy (DO)"),
                          ("RN","Registered Nurse (RN)"),
                          ("OTHER","Other"),
                         )


class License(models.Model):
    number         = models.CharField(max_length=20)
    state          = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATE_CHOICES)
    license_type   = models.CharField(max_length=5,  blank=True, default="",
                                    choices = LICENSE_TYPE_CHOICES)

    status         = models.CharField(max_length=10, choices=LICENSE_STATUS_CHOICES,
                                         default ="")
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

class Address(models.Model):
    address_type = models.CharField(max_length=12, choices=ADDRESS_TYPE_CHOICES)
    address_1    = models.CharField(max_length=200, default="")
    address_2    = models.CharField(max_length=200, blank=True, default="")
    city         = models.CharField(max_length=200, blank=True, default="")
    state        = models.CharField(max_length=2,  blank=True, default="",
                                    choices = US_STATE_CHOICES)
    zip             = models.CharField(max_length=200,  blank=True, default="")
    
    us_phone_number = models.CharField(max_length=15,  blank=True, default="")
    us_fax_number   = models.CharField(max_length=15,  blank=True, default="")

    country_code    = models.CharField(max_length=2,  blank=True, default="US",
                                    choices = COUNTRY_CHOICES)
    
    foriegn_state         = models.CharField(max_length=2,  blank=True, default="")
    foriegn_postal        = models.CharField(max_length=12,  blank=True, default="")
    foriegn_phone_number  = models.CharField(max_length=15,  blank=True, default="")
    latitude              = models.CharField(max_length=20, default="", blank=True)
    longitude             = models.CharField(max_length=20, default="", blank=True)
    foriegn_phone_number  = models.CharField(max_length=15,  blank=True, default="")
    foriegn_phone_number  = models.CharField(max_length=15,  blank=True, default="")
    website               = models.CharField(max_length=15,  blank=True, default="")
    driving_details       = models.CharField(max_length=15,  blank=True, default="")
    hours_of_operation    = models.TextField(max_length=255,  blank=True, default="")
    private_email_contact = models.CharField(max_length=15,  blank=True, default="")
    public_email_contact  = models.CharField(max_length=15,  blank=True, default="")
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
        
        if self.address_type in ("BUSINESS-DOM", "PRACTICE-DOM"):
            address = "%s %s %s, %s %s %s" % (self.address_1, self.address_2, self.city,
                                          self.state, self.zip, self.country_code)
            
        if self.address_type in ("BUSINESS-FOR", "PRACTICE-FOR"):
            address = "%s %s %s, %s %s %s" % (self.address_1, self.address_2, self.city,
                                          self.foriegn_state, self.foriegn_postal,
                                          self.country_code)

        if self.address_type in ("BUSINESS-MIL", "PRACTICE-MIL"):
            address = "%s %s %s, %s %s %s MILITARY" % (self.address_1, self.address_2,
                                                   self.city,
                                          self.state, self.zip, self.country_code)
        
        
        return address
        
        name = "UNK"
        if self.entity_type == "O":
            name = self.organization_name
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as, self.organization_name)
        elif self.entity_type == "P":
            name = "%s %s" % (self.first_name, self.last_name)
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as, self.first_name, self.last_name)
            
        e = "%s is a %s managed by %s" % (name, self.enumeration_type, self.managers)
        return e

    
    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)
        verbose_name_plural = "Addresses"


class Enumeration(models.Model):
    managers                    = models.ManyToManyField(User, null=True, blank=True)
    other_addresses             = models.ManyToManyField(Address,
                                    related_name = "enumeration_other_addresses",
                                    null=True, blank=True)
    primary_business_address    = models.ForeignKey(Address,
                                    related_name = "enumeration_primary_business_address")
    primary_practice_address    = models.ForeignKey(Address,
                                    related_name = "enumeration_primary_practice_address")
    parent_organization         = models.ForeignKey('self', null=True, blank=True,
                                    related_name = "enumeration_parent_organization")
    associations                = models.ManyToManyField('self', null=True, blank=True,
                                    related_name = "enumerations_associations")
    enumeration_type            = models.CharField(max_length=10, choices=ENUMERATION_TYPE_CHOICES,)
    licenses                    = models.ManyToManyField(License, null=True, blank=True,
                                    related_name = "enumerations_licenses")
    #entity_type                 = models.CharField(max_length=12, choices=ENTITY_CHOICES)
    tracking_number             = models.CharField(max_length=50, blank=True, default="")
    status                      = models.CharField(max_length=1, choices=ENUMERATION_STATUS_CHOICES,
                                                   default ="P", blank=True)
    reason_decactvated          = models.CharField(max_length=1, choices=DECACTIVAED_REASON_CHOICES,
                                                   default="", blank=True)
    deactivated_details         = models.TextField(max_length=1000, blank=True, default="")
    number                      = models.CharField(max_length=10, blank=True, default="")
    first_name                  = models.CharField(max_length=100, blank=True, default="")
    last_name                   = models.CharField(max_length=100, blank=True, default="")
    organization_name           = models.CharField(max_length=100, blank=True, default="")
    doing_business_as           = models.CharField(max_length=100, blank=True, default="")
    sole_protieter              = models.BooleanField(default=False)
    tein                        = models.CharField(max_length=9, blank=True, default="", verbose_name="Tax ID Number")
    ssn                         = models.CharField(max_length=10, blank=True, default="", verbose_name = "Social Security Number")
    modify_token                = models.CharField(max_length=36, blank=True, default=uuid.uuid4)
    private_email_contact       = models.CharField(max_length=150,  blank=True, default="")
    public_email_contact        = models.CharField(max_length=150,  blank=True, default="")
    primary_taxonomy            = models.ForeignKey(TaxonomyCode, null=True, blank=True, related_name ="enumeration_primary_taxonomy")
    other_taxonomies            = models.ManyToManyField(TaxonomyCode, null=True, blank=True, related_name ="enumeration_other_taxonomies")
    website                     = models.CharField(max_length=300,  blank=True, default="")
    driving_directions          = models.TextField(max_length=266,  blank=True, default="")
    hours_of_operation          = models.CharField(max_length=15,  blank=True, default="")
    private_email_contact       = models.CharField(max_length=15,  blank=True, default="")
    public_email_contact        = models.CharField(max_length=15,  blank=True, default="")
    phone_number_extension      = models.CharField(max_length=15,  blank=True, default="")
    bio                         = models.TextField(max_length=255,  blank=True, default="")
    background_image            = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="enumeration-backgrounds",
                                    verbose_name= "Background Image")
    avatar_image                = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="enumeration-avatars",
                                    verbose_name= "Profile Photo")

    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)


    def __unicode__(self):
        name = "UNK"
        if self.enumeration_type in ("HPID", "OEID-2", "NPI-2"):
            name = self.organization_name
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as, self.organization_name)
        elif self.enumeration_type in ("OEID-1", "NPI-1"):
            name = "%s %s" % (self.first_name, self.last_name)
            if self.doing_business_as:
                name = "%s (%s)" % (self.doing_business_as, self.first_name, self.last_name)
            
        e = "%s is an %s managed by %s" % (name, self.enumeration_type, ", ".join([manager.username
                                                    for manager in self.managers.all()]))
        return e