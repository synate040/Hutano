#!/usr/bin/env python
"""
Script to create default bed types for the HUTANO system.
"""
import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hutano')
sys.path.append(project_dir)
os.chdir(project_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

# Now import Django models
from core.models import BedType

def create_default_bed_types():
    """Create default bed types if they don't exist."""
    bed_types = [
        {'name': 'General', 'description': 'General ward beds'},
        {'name': 'ICU', 'description': 'Intensive Care Unit beds'},
        {'name': 'Maternity', 'description': 'Maternity ward beds'},
        {'name': 'Pediatric', 'description': 'Pediatric ward beds'},
        {'name': 'Emergency', 'description': 'Emergency department beds'},
        {'name': 'Surgical', 'description': 'Surgical ward beds'},
        {'name': 'Cardiac', 'description': 'Cardiac care beds'},
    ]

    created_count = 0
    for bed_type_data in bed_types:
        bed_type, created = BedType.objects.get_or_create(
            name=bed_type_data['name'],
            defaults={'description': bed_type_data['description']}
        )
        if created:
            print(f"✅ Created bed type: {bed_type.name}")
            created_count += 1
        else:
            print(f"📋 Bed type already exists: {bed_type.name}")

    print(f"\n🎯 Summary: {created_count} new bed types created")
    print(f"📊 Total bed types: {BedType.objects.count()}")

    # List all bed types
    print("\n📋 All bed types:")
    for bt in BedType.objects.all():
        print(f"  - {bt.name}: {bt.description}")

if __name__ == '__main__':
    create_default_bed_types()
