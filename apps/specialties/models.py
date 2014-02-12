from django.db import models

class Specialty(models.Model):
    code           = models.CharField(max_length=3, unique=True)
    description    = models.CharField(max_length=100, unique=True)
    taxonomy       = models.CharField(max_length=20, blank=True, default="")
    
    def __unicode__(self):
        return self.description

    class Meta:
        get_latest_by = "id"
        ordering = ('-id',)
        verbose_name_plural = "Specialties"
