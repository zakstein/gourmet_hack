import os
import sys
import django.core.handlers.wsgi

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

application = django.core.handlers.wsgi.WSGIHandler()

path = '/vagrant/gourmet'
if path not in sys.path:
    sys.path.append(path)

