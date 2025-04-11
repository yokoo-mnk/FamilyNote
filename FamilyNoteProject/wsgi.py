"""
WSGI config for FamilyNoteProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/minakoyokoo/FamilyNote/FamilyNoteProject')

os.environ['DJANGO_SETTINGS_MODULE'] = 'FamilyNote.settings'

from django.core.wsgi import get_wsgi_application
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyNoteProject.settings')
application = get_wsgi_application()
