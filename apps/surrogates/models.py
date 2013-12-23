from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ..enumerations.models import Enumeration


class Surrogate(models.Model):
    """This model defines which enumerations are displayed in authenticaed home
    Creating this record does not confirm the surrogate relationship. It only
    is an attempted/requested surrogate relationship. To actually mananage the
    enumeration, the user must be added as a manager on the enumeration model
    """
    user           = models.ForeignKey(User, unique=True)
    enumerations   = models.ManyToManyField(Enumeration, null=True, blank=True)
  
    
    def __unicode__(self):
        s ="Surrogate %s" % (self.user)
        return s