#!/usr/bin/env python3
"""
HUTANO Make Names Unique Script
==============================

Simple script to make all staff names unique by adding sequential numbers.

Usage:
    python make_names_unique.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Staff

def make_all_names_unique():
    """Make all staff names unique by adding sequential numbers."""
    print("🚀 Starting HUTANO Name Uniqueness Process")
    print("=" * 50)
    
    # Get all staff
    all_staff = Staff.objects.all().order_by('hospital__name', 'category__name', 'id')
    print(f"📊 Total staff to process: {all_staff.count()}")
    
    # Track used names
    used_names = set()
    updated_count = 0
    
    for i, staff in enumerate(all_staff, 1):
        original_name = staff.full_name
        base_name = original_name
        
        # Remove any existing numbers from the end
        import re
        base_name = re.sub(r'\s+\d+$', '', base_name)
        
        # Find a unique name
        counter = 1
        new_name = base_name
        
        while new_name in used_names:
            new_name = f"{base_name} {counter}"
            counter += 1
        
        # Update the staff member
        staff.full_name = new_name
        used_names.add(new_name)
        
        # Update email to match
        name_part = new_name.lower()
        # Clean up the name for email
        for title in ['dr. ', 'sister ', 'nurse ', 'tech. ', 'admin. ', 'mr. ', 'mrs. ', 'ms. ']:
            name_part = name_part.replace(title, '')
        name_part = name_part.replace(' ', '.').replace('..', '.').strip('.')
        
        hospital_part = staff.hospital.name.lower().replace(' ', '').replace('hospital', '').replace('group', '').replace('of', '')[:8]
        staff.email = f"{name_part}@{hospital_part}.co.zw"
        
        staff.save()
        
        if original_name != new_name:
            updated_count += 1
            if updated_count <= 10:  # Show first 10 changes
                print(f"   ✅ {original_name} → {new_name}")
            elif updated_count == 11:
                print(f"   ... (continuing to update remaining duplicates)")
        
        # Progress indicator
        if i % 100 == 0:
            print(f"   📈 Processed {i}/{all_staff.count()} staff members...")
    
    print(f"\n🎉 Process Complete!")
    print(f"📊 Total staff processed: {all_staff.count()}")
    print(f"🔄 Names updated: {updated_count}")
    print(f"✨ All staff now have unique names!")

if __name__ == "__main__":
    make_all_names_unique()
