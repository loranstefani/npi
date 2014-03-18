from django.db import models
from django.conf import settings


class TaxonomyCode(models.Model):

    code                = models.CharField(max_length=50, null=True, db_index=True)
    npi_worthy          = models.BooleanField(default=False)
    inactive            = models.DateField(null=True)
    description         = models.CharField(max_length=100, null=True)
    pt                  = models.CharField(max_length=30, null=True)
    taxclass            = models.CharField(max_length=30, null=True)
    speciality          = models.CharField(max_length=30, null=True, db_index=True)
    url                 = models.CharField(max_length=100, null=True)
    parent_taxonomycode_id  = models.IntegerField(max_length=11, null=True)



    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)

    def __unicode__(self):
        return "%s (%s)" % (self.description, self.code)

    class OtherTaxonomies():