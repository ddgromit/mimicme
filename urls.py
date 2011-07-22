from django.conf.urls.defaults import *
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^crossdomain.xml$',
        'flashpolicies.views.simple',
        {'domains': ['*']}),

    (r'uploadtarget','uploads.views.uploadTarget'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url(r'^uploadedmedia/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

import practice.urls
urlpatterns += practice.urls.urlpatterns

import core.urls
urlpatterns += core.urls.urlpatterns


