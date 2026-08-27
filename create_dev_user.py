import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings') # Replace 'myproject' with your project folder name
django.setup()

from django.contrib.auth.models import User

username = "admin"
password = "adminpassword123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, 'admin@example.com', password)
    print(f"Created user: {username}")
else:
    print(f"User {username} already exists.")