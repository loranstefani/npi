from django.contrib.sitemaps import Sitemap, FlatPageSitemap
from apps.enumerations.models import Enumeration
from django.core.urlresolvers import reverse



class NPISitemap(Sitemap):
    changefreq = "newer"
    priority = 0.5

    def items(self):
        return Enumeration.objects.filter(status="A")

    def lastmod(self, obj):
        return obj.updated
    
    #def location(self, obj):
    #    return "/"
    
    
class HandleSitemap(Sitemap):
    changefreq = "newer"
    priority = 0.5

    def items(self):
        return Enumeration.objects.filter(status="A")

    def lastmod(self, obj):
        return obj.updated
    
    def location(self, obj):
        return reverse('display_enumeration_profile_handle', args=[str(obj.handle)])