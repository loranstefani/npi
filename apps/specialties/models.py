from django.db import models

class Specialty(models.Model):
    code           = models.CharField(max_length=3, unique=True, db_index=True)
    description    = models.CharField(max_length=100, unique=True)
    taxonomy       = models.CharField(max_length=20, blank=True, default="", db_index=True)
    
    def __unicode__(self):
        return self.description

    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)
        verbose_name_plural = "Specialties"
