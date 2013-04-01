from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gourmet.views.home', name='home'),
    # url(r'^gourmet/', include('gourmet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('userena.urls')),
	url(r'^home/', TemplateView.as_view(template_name='home.html')),
	url(r'^about_us/', TemplateView.as_view(template_name='about_us.html')),
	)
