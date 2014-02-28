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
    
    def __unicode__(self):
        return self.identifier

    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)

