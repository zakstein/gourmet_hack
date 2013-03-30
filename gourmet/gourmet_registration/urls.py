from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gourmet.views.home', name='home'),
    # url(r'^gourmet/', include('gourmet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:

        url(r'^login/', direct_to_template,{'template':'registration/login.html'}),
)
