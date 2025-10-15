import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from django.contrib.auth.models import User

# Check if admin user exists
if User.objects.filter(username='admin').exists():
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.save()
    print("Admin user password reset to 'admin123'")
else:
    # Create a superuser
    User.objects.create_superuser('admin', 'admin@hutano.co.zw', 'admin123')
    print("Admin user created with username 'admin' and password 'admin123'")
