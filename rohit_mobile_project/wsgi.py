"""
WSGI config for rohit_mobile_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rohit_mobile_project.settings')

application = get_wsgi_application()
