from django.db import models
from ..addresses.models import US_STATE_CHOICES

IDENTIFIER_CODE_CHOICES =(("", "Blank"),("01", "Other"),("02","Medicare UPIN"),
    ("04","Medicare ID Type Unspecified"),("05", "Medicaid"),
    ("06", "Medicare OSCAR/certification"), ("07", "Medicare NSC"),
    ("08", "MEDICARE PIN"))

class Identifier(models.Model):
    identifier   = models.CharField(max_length=20,db_index=True)
    code         = models.CharField(max_length=2, choices=IDENTIFIER_CODE_CHOICES,
                                    blank=True, default="")
    state        = models.CharField(max_length=2, blank=True, default="",
                                    choices=US_STATE_CHOICES)
    issuer       = models.CharField(max_length=150, blank=True, default="" )
    added        = models.DateField(auto_now_add=True)
    updated      = models.DateField(auto_now=True)
    last_updated_ip     = models.CharField(max_length=20, blank=True,
                                default="", db_index=True)
    
    def __unicode__(self):
        i = "%s/%s/%s/%s/%s" % (self.identifier, self.issuer, self.state,
                             self.get_code_display(), self.updated)
        return i
    
    def pretty_identifier(self):
        i = """%s is a "%s" issued by %s in %s was last updated on %s.""" % \
                            (self.identifier, self.get_code_display(), self.issuer,
                             self.get_state_display(), self.updated)
        return i

    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)

