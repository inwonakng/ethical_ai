"""
WSGI config for ethicssite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

# sys.path.append('/home/usr/local/lib/python3.6/dist-packages')
sys.path.append('/home/inwon/ETHICAL_AI/ethical_ai')

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ethicssite.settings')

application = get_wsgi_application()
