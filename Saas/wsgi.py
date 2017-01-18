"""
WSGI config for Saas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os,sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workscape = os.path.dirname(project)

sys.path.append(workscape)
sys.path.append(project)

sys.path.append('/home/mbsl')






from django.core.wsgi import get_wsgi_application
#from django.core.handlers.wsgi import  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Saas.settings")

application = get_wsgi_application()
