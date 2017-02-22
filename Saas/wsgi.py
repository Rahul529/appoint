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

sys.path.append('/home/mbsl/')


import site
site.addsitedir('/.virtualenv/Saas/Saas/local/lib/python2.7/site-packages')



from django.core.wsgi import get_wsgi_application
#from django.core.handlers.wsgi import  
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Saas.settings")
#activate_env=os.path.expanauser("~/.virtualenv/Saas/Saas/bin/activate_this.py")
#execfile(activate_env,dict(__file__=activate_env))

application = get_wsgi_application()
import django.core.handlers.wsgi
application=django.core.handlers.wsgi.WSGIHandler()
