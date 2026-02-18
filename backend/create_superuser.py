#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eraride.settings')
django.setup()

from users.models import User

if not User.objects.filter(email='admin@geu.ac.in').exists():
    User.objects.create_superuser(
        email='admin@geu.ac.in',
        password='admin123',
        name='Admin User',
        phone='9999999999',
        college_id='ADMIN001',
        course='Administration',
        year=1
    )
    print("✅ Superuser created: admin@geu.ac.in / admin123")
else:
    print("⚠️  Superuser already exists")
