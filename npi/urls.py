from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from apps.enumerations.views import search_enumeration
from apps.profilee.views import display_enumeration_profile_handle, display_enumeration_profile
from django.conf.urls.static import static
from ajax_select import urls as ajax_select_urls
from sitemaps import NPISitemap, HandleSitemap
from django.contrib.sitemaps import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

sitemaps = {
  'npi':    NPISitemap,
  'handle': HandleSitemap,
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'npi.views.home', name='home'),
    # url(r'^npi/', include('npi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^$',   TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^$',              include('apps.home.urls')),
    url(r'^api/',            include('apps.api.urls')),
    url(r'^accounts/',      include('apps.accounts.urls')),
    url(r'^downloads/',     include('apps.downloads.urls')),
    url(r'^statistics/',    include('apps.statistics.urls')),
    url(r'^search/',        search_enumeration, name = "search"),
    url(r'^admin/',         include(admin.site.urls)),
    url(r'^enumerations/',  include('apps.enumerations.urls')),
    url(r'^licenses/',      include('apps.licenses.urls')),
    url(r'^direct/',        include('apps.direct.urls')),
    url(r'^surrogates/',    include('apps.surrogates.urls')),
    url(r'^identifiers/',   include('apps.identifiers.urls')),
    url(r'^reports/',       include('apps.reports.urls')),
    url(r'^dmf/',           include('apps.dmf.urls')),
    url(r'^email-campaign/', include('apps.email_campaign.urls')),
    (r'^admin/lookups/',    include(ajax_select_urls)),
    (r'^admin/',            include(admin.site.urls)),
    
    url(r'^profile/',       include('apps.profilee.urls')),
    url(r'^npi/(?P<number>\S+)/$', display_enumeration_profile,
                        name="display_enumeration_profile"),
    
    url(r'^p/(?P<handle>\S+)/$', display_enumeration_profile_handle,
                        name="display_enumeration_profile_handle"),
    
    url(r'^sitemap\.xml$', views.index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap, {'sitemaps': sitemaps}),
    

    
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
