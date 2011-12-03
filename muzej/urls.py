from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

import ajax_select.urls

admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'muzej.views.home', name='home'),
	# url(r'^muzej/', include('muzej.foo.urls')),
	
	url(r'^vhod/([0-9]+)/', 'muzej.inventura.views.vhod'),
	url(r'^[vV]/([0-9]+)/?', 'muzej.inventura.views.vhod_short'),
	url(r'^[iI]/([0-9]+)/?', 'muzej.inventura.views.primerek_short'),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^admin/lookups/', include(ajax_select.urls)),
)
