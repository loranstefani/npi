from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from apps.enumerations.views import search_enumeration
from django.conf.urls.static import static
from ajax_select import urls as ajax_select_urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'npi.views.home', name='home'),
    # url(r'^npi/', include('npi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^$',   TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^$',              include('apps.home.urls')),
    url(r'^accounts/',      include('apps.accounts.urls')),
    url(r'^downloads/',     include('apps.downloads.urls')),
    url(r'^statistics/',    include('apps.statistics.urls')),
    url(r'^search/',        search_enumeration, name = "search"),
    url(r'^admin/',         include(admin.site.urls)),
    url(r'^enumerations/',  include('apps.enumerations.urls')),
    url(r'^licenses/',      include('apps.licenses.urls')),
    url(r'^direct/',        include('apps.direct.urls')),
    url(r'^profile/',       include('apps.profilee.urls')),
    url(r'^surrogates/',    include('apps.surrogates.urls')),
    (r'^admin/lookups/',    include(ajax_select_urls)),
    (r'^admin/',            include(admin.site.urls)),
    
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
