from django.db import models
from django.conf import settings


class DeceasedMasterFile(models.Model):
    file = models.FileField(
                    max_length=255L, upload_to="dmf",
                    verbose_name= "Decesed Master File",
                    help_text ="Typicaly process this 1x per week with SSA provided DMF file.",)
    processed     = models.BooleanField(default = False, blank = True, editable=False)
    added         = models.DateField(auto_now_add = True)
    updated       = models.DateField(auto_now = True)
    
    class Meta:
    
        ordering = ('updated',)

    def __unicode__(self):
        f ="%s" % (self.file)
        return f


