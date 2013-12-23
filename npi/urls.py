from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

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
    url(r'^$',   include('apps.home.urls')),
    url(r'^accounts/',   include('apps.accounts.urls')),
    url(r'^downloads/',   include('apps.downloads.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^enumerations/', include('apps.enumerations.urls')),
)
