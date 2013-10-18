from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/signin/', 'userena.views.signin', {'template_name': 'custom_signin.html'}),
    url(r'^accounts/', include('userena.urls')),
	url(r'^/?$', 'restaurant_list.views.display_home_page'),
	url(r'^about_us/', TemplateView.as_view(template_name='about_us.html')),

    url(r'^list/$', 'restaurant_list.views.display_restaurant_list_and_upload_for_current_user'),
    url(r'^list/(?P<user_to_display>\d+)$', 'restaurant_list.views.display_restaurant_list_and_upload_for_user'),

    url(r'^restaurant_list/$', 'restaurant_list.views.display_restaurant_list_for_current_user'),
    url(r'^restaurant_list/(?P<user_to_display>\d+)$', 'restaurant_list.views.display_restaurant_list_for_user'),

    # url(r'^show_restaurant_search/$', 'restaurant_list.views.show_restaurant_search'),
    # url(r'^show_restaurant_search/(?P<restaurant_list_element_id>\d+)$', 'restaurant_list.views.show_restaurant_search'),

    url(r'^restaurant_search/$', 'restaurant_list.views.restaurant_search'),

    url(r'^upload/$', 'restaurant_list.views.upload_restaurant_list_from_file'),
    url(r'^add/$', 'restaurant_list.views.add_restaurant_to_list'),

    url(r'^edit/$', 'restaurant_list.views.edit_restaurant_list_element'),

    url(r'^delete/$', 'restaurant_list.views.delete_restaurant_from_list'),

	url(r'^styleguide/', TemplateView.as_view(template_name='styleguide.html')),
)

