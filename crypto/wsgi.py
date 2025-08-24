"""
WSGI config for crypto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto.settings')
django.setup()

# Auto-run migrations on startup (only do this if you can't access shell)
try:
    call_command("migrate", interactive=False)
except Exception as e:
    print(f"Migration error: {e}")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
