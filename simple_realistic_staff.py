import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff, StaffCategory, Department

print("🔄 Creating realistic staff distribution...")

# Clear existing staff
Staff.objects.all().delete()
print("✅ Cleared existing staff")

# Create categories
categories = {}
for cat_name in ['Physicians', 'Nurses', 'Technicians', 'Administrative Staff', 'Support Staff']:
    categories[cat_name], _ = StaffCategory.objects.get_or_create(name=cat_name)

# Shona names
shona_names = [
    'Dr. Tendai Mukamuri', 'Dr. Chipo Mutasa', 'Dr. Blessing Chikwanha', 'Dr. Tarisai Moyo',
    'Dr. Fungai Sibanda', 'Dr. Rutendo Ncube', 'Dr. Takudzwa Mpofu', 'Dr. Nyasha Dube',
    'Sister Chipo Nyathi', 'Nurse Tendai Nyathi', 'Sister Blessing Nyathi', 'Nurse Rutendo Nyathi',
    'Sister Nyasha Nyathi', 'Nurse Chiedza Nyathi', 'Sister Tsitsi Nyathi', 'Nurse Rumbidzai Nyathi',
    'Sister Rudo Nyathi', 'Nurse Tarisai Nyathi', 'Sister Fungai Nyathi', 'Nurse Takudzwa Nyathi',
    'Sister Chengetai Nyathi', 'Nurse Tinashe Nyathi', 'Sister Munyaradzi Nyathi', 'Nurse Farai Nyathi',
    'Tech. Tendai Mukamuri', 'Tech. Blessing Chikwanha', 'Tech. Nyasha Mutasa', 'Tech. Rutendo Moyo',
    'Tech. Chipo Sibanda', 'Tech. Tarisai Ncube', 'Tech. Fungai Mpofu', 'Tech. Chengetai Dube',
    'Admin. Chipo Mukamuri', 'Admin. Tendai Chikwanha', 'Admin. Blessing Mutasa', 'Admin. Nyasha Moyo',
    'Admin. Rutendo Sibanda', 'Admin. Tarisai Ncube', 'Admin. Fungai Mpofu', 'Admin. Chengetai Dube',
    'Support. Chipo Moyo', 'Support. Tendai Moyo', 'Support. Blessing Moyo', 'Support. Nyasha Moyo',
    'Support. Rutendo Moyo', 'Support. Tarisai Moyo', 'Support. Fungai Moyo', 'Support. Chengetai Moyo'
]

# Ndebele names
ndebele_names = [
    'Dr. Sipho Ncube', 'Dr. Nomsa Mpofu', 'Dr. Thabo Dube', 'Dr. Busisiwe Ndlovu',
    'Dr. Mandla Sibanda', 'Dr. Nokuthula Moyo', 'Dr. Sizani Nkomo', 'Dr. Themba Khumalo',
    'Sister Nomsa Nyathi', 'Nurse Sipho Nyathi', 'Sister Busisiwe Nyathi', 'Nurse Thabo Nyathi',
    'Sister Mandla Nyathi', 'Nurse Nokuthula Nyathi', 'Sister Sizani Nyathi', 'Nurse Themba Nyathi',
    'Sister Nomthandazo Nyathi', 'Nurse Bhekani Nyathi', 'Sister Sithabile Nyathi', 'Nurse Mthokozisi Nyathi',
    'Sister Nompumelelo Nyathi', 'Nurse Sabelo Nyathi', 'Sister Thandiwe Nyathi', 'Nurse Nkosana Nyathi',
    'Tech. Sipho Ncube', 'Tech. Nomsa Mpofu', 'Tech. Thabo Dube', 'Tech. Busisiwe Ndlovu',
    'Tech. Mandla Sibanda', 'Tech. Nokuthula Moyo', 'Tech. Sizani Nkomo', 'Tech. Themba Khumalo',
    'Admin. Nomsa Ncube', 'Admin. Sipho Mpofu', 'Admin. Busisiwe Dube', 'Admin. Thabo Ndlovu',
    'Admin. Mandla Sibanda', 'Admin. Nokuthula Moyo', 'Admin. Sizani Nkomo', 'Admin. Themba Khumalo',
    'Support. Nomsa Ncube', 'Support. Sipho Mpofu', 'Support. Busisiwe Dube', 'Support. Thabo Ndlovu',
    'Support. Mandla Sibanda', 'Support. Nokuthula Moyo', 'Support. Sizani Nkomo', 'Support. Themba Khumalo'
]

# Hospital staff configurations (realistic numbers)
hospital_configs = {
    'Parirenyatwa Group of Hospitals': {'total': 565, 'type': 'Major Referral Hospital'},
    'Sally Mugabe Central Hospital': {'total': 518, 'type': 'Major Referral Hospital'},
    'Mpilo Central Hospital': {'total': 482, 'type': 'Major Referral Hospital'},
    'United Bulawayo Hospitals': {'total': 452, 'type': 'Major Referral Hospital'},
    'Chitungwiza Central Hospital': {'total': 323, 'type': 'Provincial Hospital'},
    'Gweru Provincial Hospital': {'total': 280, 'type': 'Provincial Hospital'},
    'Bindura Provincial Hospital': {'total': 239, 'type': 'Provincial Hospital'},
    'Karanda Mission Hospital': {'total': 150, 'type': 'Mission Hospital'},
    'Test Hospital for ML Demo': {'total': 88, 'type': 'Test Hospital'}
}

hospitals = Hospital.objects.all()
print(f"📋 Found {hospitals.count()} hospitals")

staff_counter = 1
total_created = 0

for hospital in hospitals:
    hospital_name = hospital.name
    
    # Get configuration
    if hospital_name in hospital_configs:
        config = hospital_configs[hospital_name]
        total_staff = config['total']
        hospital_type = config['type']
    else:
        total_staff = 200  # Default
        hospital_type = 'District Hospital'
    
    print(f"\n🏥 {hospital_name}")
    print(f"   🏷️ Type: {hospital_type}")
    print(f"   👥 Target Staff: {total_staff}")
    
    # Determine names based on location
    hospital_name_lower = hospital_name.lower()
    if any(word in hospital_name_lower for word in ['harare', 'sally mugabe', 'parirenyatwa', 'chitungwiza']):
        names = shona_names
        culture = "Shona"
    elif any(word in hospital_name_lower for word in ['bulawayo', 'mpilo', 'united bulawayo']):
        names = ndebele_names
        culture = "Ndebele"
    else:
        names = shona_names + ndebele_names
        culture = "Mixed"
    
    print(f"   🌍 Using {culture} names")
    
    # Create departments
    dept_names = ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU', 'Laboratory', 'Radiology']
    departments = []
    for dept_name in dept_names:
        dept, _ = Department.objects.get_or_create(
            hospital=hospital,
            name=dept_name,
            defaults={'description': f'{dept_name} department'}
        )
        departments.append(dept)
    
    # Calculate staff distribution (realistic ratios)
    physicians = max(int(total_staff * 0.15), 8)  # 15% physicians
    nurses = max(int(total_staff * 0.45), 20)     # 45% nurses
    technicians = max(int(total_staff * 0.20), 10) # 20% technicians
    admin = max(int(total_staff * 0.08), 5)       # 8% admin
    support = total_staff - physicians - nurses - technicians - admin  # Remaining
    
    staff_distribution = [
        (categories['Physicians'], physicians),
        (categories['Nurses'], nurses),
        (categories['Technicians'], technicians),
        (categories['Administrative Staff'], admin),
        (categories['Support Staff'], support)
    ]
    
    hospital_staff_created = 0
    
    for category, count in staff_distribution:
        # Create staff with diverse names
        for i in range(count):
            # Cycle through names and add variations
            name_index = i % len(names)
            base_name = names[name_index]
            
            # Add slight variations for repeated names
            if i >= len(names):
                cycle = i // len(names)
                if cycle == 1:
                    # Add middle initial
                    parts = base_name.split(' ')
                    if len(parts) >= 2:
                        base_name = f"{parts[0]} {chr(65 + (i % 26))}. {' '.join(parts[1:])}"
                elif cycle == 2:
                    # Add Jr./Sr.
                    base_name = f"{base_name} Jr."
            
            department = random.choice(departments)
            
            staff = Staff.objects.create(
                hospital=hospital,
                department=department,
                category=category,
                staff_id=f'STF-{hospital.id:02d}-{staff_counter:04d}',
                full_name=base_name,
                position='Staff Member',
                contact_number=f'+263{random.randint(700000000, 799999999)}',
                email=f"staff{staff_counter}@{hospital.name.lower().replace(' ', '').replace('hospital', '').replace('group', '').replace('of', '')[:10]}.co.zw",
                is_active=True
            )
            
            staff_counter += 1
            total_created += 1
            hospital_staff_created += 1
        
        print(f"   ✅ Created {count} {category.name}")
    
    print(f"   📊 Total created: {hospital_staff_created}")

print(f"\n🎉 Successfully created {total_created} staff members with realistic distribution!")

# Show summary
print("\n📋 Final Summary:")
for hospital in hospitals:
    total_staff = Staff.objects.filter(hospital=hospital).count()
    hospital_type = hospital_configs.get(hospital.name, {}).get('type', 'District Hospital')
    print(f"🏥 {hospital.name} ({hospital_type}): {total_staff} staff")

print("\n✅ Realistic staff distribution complete!")
