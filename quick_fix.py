import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff, StaffCategory, Department

# Clear existing staff
Staff.objects.all().delete()
print("Cleared staff")

# Create categories
cat_physicians, _ = StaffCategory.objects.get_or_create(name='Physicians')
cat_nurses, _ = StaffCategory.objects.get_or_create(name='Nurses')

# Hospital configurations
configs = {
    'Parirenyatwa Group of Hospitals': 565,
    'Sally Mugabe Central Hospital': 518, 
    'Mpilo Central Hospital': 482,
    'United Bulawayo Hospitals': 452,
    'Chitungwiza Central Hospital': 323,
    'Gweru Provincial Hospital': 280,
    'Bindura Provincial Hospital': 239,
    'Karanda Mission Hospital': 150,
    'Test Hospital for ML Demo': 88
}

# Simple names
shona_names = ['Dr. Tendai Mukamuri', 'Dr. Chipo Mutasa', 'Sister Nyasha Nyathi', 'Nurse Rutendo Nyathi']
ndebele_names = ['Dr. Sipho Ncube', 'Dr. Nomsa Mpofu', 'Sister Busisiwe Nyathi', 'Nurse Thabo Nyathi']

counter = 1

for hospital in Hospital.objects.all():
    target_staff = configs.get(hospital.name, 200)
    print(f"Creating {target_staff} staff for {hospital.name}")
    
    # Choose names based on location
    if any(word in hospital.name.lower() for word in ['harare', 'sally', 'parirenyatwa', 'chitungwiza']):
        names = shona_names
    elif any(word in hospital.name.lower() for word in ['bulawayo', 'mpilo']):
        names = ndebele_names
    else:
        names = shona_names + ndebele_names
    
    # Get or create department
    dept, _ = Department.objects.get_or_create(
        hospital=hospital, 
        name='General',
        defaults={'description': 'General department'}
    )
    
    # Create staff
    for i in range(target_staff):
        name = names[i % len(names)]
        
        # Determine category
        if name.startswith('Dr.'):
            category = cat_physicians
        else:
            category = cat_nurses
        
        Staff.objects.create(
            hospital=hospital,
            department=dept,
            category=category,
            staff_id=f'STF-{hospital.id:02d}-{counter:04d}',
            full_name=name,
            position='Staff Member',
            contact_number=f'+263771234567',
            email=f'staff{counter}@hospital.co.zw',
            is_active=True
        )
        counter += 1
    
    actual_count = Staff.objects.filter(hospital=hospital).count()
    print(f"  Created {actual_count} staff members")

total_staff = Staff.objects.count()
print(f"\nTotal staff created: {total_staff}")

# Show summary
print("\nHospital Summary:")
for hospital in Hospital.objects.all():
    count = Staff.objects.filter(hospital=hospital).count()
    print(f"{hospital.name}: {count} staff")

print("Done!")
