"""
WSGI config for ocrweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/html/ocrweb/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocrweb.settings')

application = get_wsgi_application()
