from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
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
	url(r'^/?$', TemplateView.as_view(template_name='home.html')),
	url(r'^about_us/', TemplateView.as_view(template_name='about_us.html')),
    url(r'^list/$', 'restaurant_list.views.display_restaurant_list_and_upload'),
    url(r'^restaurant_list/$', 'restaurant_list.views.display_restaurant_list'),
    url(r'^upload/$', 'restaurant_list.views.upload_restaurant_list_from_file'),
	url(r'^styleguide/', TemplateView.as_view(template_name='styleguide.html')),
)

