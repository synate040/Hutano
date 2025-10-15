import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff, StaffCategory, Department

print("🔄 Creating realistic staff distribution across hospitals...")

# Clear existing staff
Staff.objects.all().delete()
print("✅ Cleared existing staff")

# Create categories
categories = {}
for cat_name in ['Physicians', 'Nurses', 'Technicians', 'Administrative Staff', 'Support Staff']:
    categories[cat_name], _ = StaffCategory.objects.get_or_create(name=cat_name)

# Comprehensive Shona names (for Harare hospitals)
shona_names = {
    'physicians': [
        'Dr. Tendai Mukamuri', 'Dr. Chipo Mutasa', 'Dr. Blessing Chikwanha', 'Dr. Tarisai Moyo',
        'Dr. Fungai Sibanda', 'Dr. Rutendo Ncube', 'Dr. Takudzwa Mpofu', 'Dr. Nyasha Dube',
        'Dr. Chengetai Ndlovu', 'Dr. Tinashe Mujuru', 'Dr. Chiedza Makoni', 'Dr. Tafadzwa Gumbo',
        'Dr. Rumbidzai Chigumira', 'Dr. Munyaradzi Mapfumo', 'Dr. Tsitsi Chidzonga', 'Dr. Farai Mukamuri',
        'Dr. Rudo Chikwanha', 'Dr. Simba Mutasa', 'Dr. Patience Mukamuri', 'Dr. Memory Chikwanha',
        'Dr. Clever Mutasa', 'Dr. Precious Moyo', 'Dr. Gift Sibanda', 'Dr. Loveness Ncube',
        'Dr. Godwin Mpofu', 'Dr. Mercy Dube', 'Dr. Justice Ndlovu', 'Dr. Brighton Mujuru',
        'Dr. Gracious Makoni', 'Dr. Honest Gumbo', 'Dr. Perseverance Chigumira', 'Dr. Wisdom Mapfumo',
        'Dr. Faith Chidzonga', 'Dr. Hope Mukamuri', 'Dr. Peace Chikwanha', 'Dr. Joy Mutasa',
        'Dr. Trust Moyo', 'Dr. Courage Sibanda', 'Dr. Prosper Ncube', 'Dr. Success Mpofu',
        'Dr. Fortunate Mukamuri', 'Dr. Innocent Chikwanha', 'Dr. Grateful Mutasa', 'Dr. Wonderful Moyo'
    ],
    'nurses': [
        'Sister Chipo Nyathi', 'Nurse Tendai Nyathi', 'Sister Blessing Nyathi', 'Nurse Rutendo Nyathi',
        'Sister Nyasha Nyathi', 'Nurse Chiedza Nyathi', 'Sister Tsitsi Nyathi', 'Nurse Rumbidzai Nyathi',
        'Sister Rudo Nyathi', 'Nurse Tarisai Nyathi', 'Sister Fungai Nyathi', 'Nurse Takudzwa Nyathi',
        'Sister Chengetai Nyathi', 'Nurse Tinashe Nyathi', 'Sister Munyaradzi Nyathi', 'Nurse Farai Nyathi',
        'Sister Tafadzwa Nyathi', 'Nurse Simba Nyathi', 'Sister Patience Nyathi', 'Nurse Memory Nyathi',
        'Sister Clever Nyathi', 'Nurse Precious Nyathi', 'Sister Gift Nyathi', 'Nurse Loveness Nyathi',
        'Sister Godwin Nyathi', 'Nurse Mercy Nyathi', 'Sister Justice Nyathi', 'Nurse Brighton Nyathi',
        'Sister Gracious Nyathi', 'Nurse Honest Nyathi', 'Sister Perseverance Nyathi', 'Nurse Wisdom Nyathi',
        'Sister Faith Nyathi', 'Nurse Hope Nyathi', 'Sister Peace Nyathi', 'Nurse Joy Nyathi',
        'Sister Trust Nyathi', 'Nurse Courage Nyathi', 'Sister Prosper Nyathi', 'Nurse Success Nyathi',
        'Sister Fortunate Nyathi', 'Nurse Innocent Nyathi', 'Sister Grateful Nyathi', 'Nurse Wonderful Nyathi',
        'Sister Chipo Mukamuri', 'Nurse Tendai Mukamuri', 'Sister Blessing Mukamuri', 'Nurse Rutendo Mukamuri',
        'Sister Nyasha Mukamuri', 'Nurse Chiedza Mukamuri', 'Sister Tsitsi Mukamuri', 'Nurse Rumbidzai Mukamuri',
        'Sister Rudo Mukamuri', 'Nurse Tarisai Mukamuri', 'Sister Fungai Mukamuri', 'Nurse Takudzwa Mukamuri',
        'Sister Chengetai Mukamuri', 'Nurse Tinashe Mukamuri', 'Sister Munyaradzi Mukamuri', 'Nurse Farai Mukamuri',
        'Sister Tafadzwa Mukamuri', 'Nurse Simba Mukamuri', 'Sister Patience Mukamuri', 'Nurse Memory Mukamuri'
    ],
    'technicians': [
        'Tech. Tendai Mukamuri', 'Tech. Blessing Chikwanha', 'Tech. Nyasha Mutasa', 'Tech. Rutendo Moyo',
        'Tech. Chipo Sibanda', 'Tech. Tarisai Ncube', 'Tech. Fungai Mpofu', 'Tech. Chengetai Dube',
        'Tech. Takudzwa Ndlovu', 'Tech. Chiedza Mujuru', 'Tech. Tsitsi Makoni', 'Tech. Rumbidzai Gumbo',
        'Tech. Tinashe Chigumira', 'Tech. Rudo Mapfumo', 'Tech. Munyaradzi Chidzonga', 'Tech. Farai Mukamuri',
        'Tech. Tafadzwa Chikwanha', 'Tech. Simba Mutasa', 'Tech. Patience Mukamuri', 'Tech. Memory Chikwanha',
        'Tech. Clever Mutasa', 'Tech. Precious Moyo', 'Tech. Gift Sibanda', 'Tech. Loveness Ncube',
        'Tech. Godwin Mpofu', 'Tech. Mercy Dube', 'Tech. Justice Ndlovu', 'Tech. Brighton Mujuru'
    ],
    'admin': [
        'Admin. Chipo Mukamuri', 'Admin. Tendai Chikwanha', 'Admin. Blessing Mutasa', 'Admin. Nyasha Moyo',
        'Admin. Rutendo Sibanda', 'Admin. Tarisai Ncube', 'Admin. Fungai Mpofu', 'Admin. Chengetai Dube',
        'Admin. Chiedza Ndlovu', 'Admin. Takudzwa Mujuru', 'Admin. Tsitsi Makoni', 'Admin. Rumbidzai Gumbo',
        'Admin. Tinashe Chigumira', 'Admin. Rudo Mapfumo', 'Admin. Munyaradzi Chidzonga', 'Admin. Farai Mukamuri'
    ],
    'support': [
        'Support. Chipo Moyo', 'Support. Tendai Moyo', 'Support. Blessing Moyo', 'Support. Nyasha Moyo',
        'Support. Rutendo Moyo', 'Support. Tarisai Moyo', 'Support. Fungai Moyo', 'Support. Chengetai Moyo',
        'Support. Chiedza Moyo', 'Support. Takudzwa Moyo', 'Support. Tsitsi Moyo', 'Support. Rumbidzai Moyo',
        'Support. Tinashe Moyo', 'Support. Rudo Moyo', 'Support. Munyaradzi Moyo', 'Support. Farai Moyo',
        'Support. Tafadzwa Moyo', 'Support. Simba Moyo', 'Support. Patience Moyo', 'Support. Memory Moyo'
    ]
}

# Comprehensive Ndebele names (for Bulawayo hospitals)
ndebele_names = {
    'physicians': [
        'Dr. Sipho Ncube', 'Dr. Nomsa Mpofu', 'Dr. Thabo Dube', 'Dr. Busisiwe Ndlovu',
        'Dr. Mandla Sibanda', 'Dr. Nokuthula Moyo', 'Dr. Sizani Nkomo', 'Dr. Themba Khumalo',
        'Dr. Nomthandazo Mthembu', 'Dr. Bhekani Nyathi', 'Dr. Sithabile Tshuma', 'Dr. Mthokozisi Mlilo',
        'Dr. Nompumelelo Ngwenya', 'Dr. Sabelo Masuku', 'Dr. Thandiwe Mhlanga', 'Dr. Nkosana Ndiweni',
        'Dr. Sindisiwe Nkala', 'Dr. Mduduzi Gumede', 'Dr. Nomsa Nyathi', 'Dr. Sipho Nyathi',
        'Dr. Thabo Nyathi', 'Dr. Busisiwe Nyathi', 'Dr. Mandla Nyathi', 'Dr. Nokuthula Nyathi',
        'Dr. Sizani Nyathi', 'Dr. Themba Nyathi', 'Dr. Nomthandazo Nyathi', 'Dr. Bhekani Nyathi',
        'Dr. Sithabile Nyathi', 'Dr. Mthokozisi Nyathi', 'Dr. Nompumelelo Nyathi', 'Dr. Sabelo Nyathi',
        'Dr. Thandiwe Nyathi', 'Dr. Nkosana Nyathi', 'Dr. Sindisiwe Nyathi', 'Dr. Mduduzi Nyathi',
        'Dr. Nomsa Tshuma', 'Dr. Sipho Tshuma', 'Dr. Thabo Tshuma', 'Dr. Busisiwe Tshuma'
    ],
    'nurses': [
        'Sister Nomsa Nyathi', 'Nurse Sipho Nyathi', 'Sister Busisiwe Nyathi', 'Nurse Thabo Nyathi',
        'Sister Mandla Nyathi', 'Nurse Nokuthula Nyathi', 'Sister Sizani Nyathi', 'Nurse Themba Nyathi',
        'Sister Nomthandazo Nyathi', 'Nurse Bhekani Nyathi', 'Sister Sithabile Nyathi', 'Nurse Mthokozisi Nyathi',
        'Sister Nompumelelo Nyathi', 'Nurse Sabelo Nyathi', 'Sister Thandiwe Nyathi', 'Nurse Nkosana Nyathi',
        'Sister Sindisiwe Nyathi', 'Nurse Mduduzi Nyathi', 'Sister Nomsa Tshuma', 'Nurse Sipho Tshuma',
        'Sister Busisiwe Tshuma', 'Nurse Thabo Tshuma', 'Sister Mandla Tshuma', 'Nurse Nokuthula Tshuma',
        'Sister Sizani Tshuma', 'Nurse Themba Tshuma', 'Sister Nomthandazo Tshuma', 'Nurse Bhekani Tshuma',
        'Sister Sithabile Tshuma', 'Nurse Mthokozisi Tshuma', 'Sister Nompumelelo Tshuma', 'Nurse Sabelo Tshuma',
        'Sister Thandiwe Tshuma', 'Nurse Nkosana Tshuma', 'Sister Sindisiwe Tshuma', 'Nurse Mduduzi Tshuma',
        'Sister Nomsa Ncube', 'Nurse Sipho Ncube', 'Sister Busisiwe Ncube', 'Nurse Thabo Ncube',
        'Sister Mandla Ncube', 'Nurse Nokuthula Ncube', 'Sister Sizani Ncube', 'Nurse Themba Ncube',
        'Sister Nomthandazo Ncube', 'Nurse Bhekani Ncube', 'Sister Sithabile Ncube', 'Nurse Mthokozisi Ncube',
        'Sister Nompumelelo Ncube', 'Nurse Sabelo Ncube', 'Sister Thandiwe Ncube', 'Nurse Nkosana Ncube',
        'Sister Sindisiwe Ncube', 'Nurse Mduduzi Ncube', 'Sister Nomsa Mpofu', 'Nurse Sipho Mpofu',
        'Sister Busisiwe Mpofu', 'Nurse Thabo Mpofu', 'Sister Mandla Mpofu', 'Nurse Nokuthula Mpofu'
    ],
    'technicians': [
        'Tech. Sipho Ncube', 'Tech. Nomsa Mpofu', 'Tech. Thabo Dube', 'Tech. Busisiwe Ndlovu',
        'Tech. Mandla Sibanda', 'Tech. Nokuthula Moyo', 'Tech. Sizani Nkomo', 'Tech. Themba Khumalo',
        'Tech. Nomthandazo Mthembu', 'Tech. Bhekani Nyathi', 'Tech. Sithabile Tshuma', 'Tech. Mthokozisi Mlilo',
        'Tech. Nompumelelo Ngwenya', 'Tech. Sabelo Masuku', 'Tech. Thandiwe Mhlanga', 'Tech. Nkosana Ndiweni',
        'Tech. Sindisiwe Nkala', 'Tech. Mduduzi Gumede', 'Tech. Nomsa Nyathi', 'Tech. Sipho Nyathi',
        'Tech. Thabo Nyathi', 'Tech. Busisiwe Nyathi', 'Tech. Mandla Nyathi', 'Tech. Nokuthula Nyathi'
    ],
    'admin': [
        'Admin. Nomsa Ncube', 'Admin. Sipho Mpofu', 'Admin. Busisiwe Dube', 'Admin. Thabo Ndlovu',
        'Admin. Mandla Sibanda', 'Admin. Nokuthula Moyo', 'Admin. Sizani Nkomo', 'Admin. Themba Khumalo',
        'Admin. Nomthandazo Mthembu', 'Admin. Bhekani Nyathi', 'Admin. Sithabile Tshuma', 'Admin. Mthokozisi Mlilo',
        'Admin. Nompumelelo Ngwenya', 'Admin. Sabelo Masuku', 'Admin. Thandiwe Mhlanga', 'Admin. Nkosana Ndiweni'
    ],
    'support': [
        'Support. Nomsa Ncube', 'Support. Sipho Mpofu', 'Support. Busisiwe Dube', 'Support. Thabo Ndlovu',
        'Support. Mandla Sibanda', 'Support. Nokuthula Moyo', 'Support. Sizani Nkomo', 'Support. Themba Khumalo',
        'Support. Nomthandazo Mthembu', 'Support. Bhekani Nyathi', 'Support. Sithabile Tshuma', 'Support. Mthokozisi Mlilo',
        'Support. Nompumelelo Ngwenya', 'Support. Sabelo Masuku', 'Support. Thandiwe Mhlanga', 'Support. Nkosana Ndiweni',
        'Support. Sindisiwe Nkala', 'Support. Mduduzi Gumede', 'Support. Nomsa Nyathi', 'Support. Sipho Nyathi'
    ]
}

# REALISTIC HOSPITAL STAFF DISTRIBUTION based on hospital size and type
hospital_configurations = {
    # MAJOR REFERRAL HOSPITALS (Largest)
    'Parirenyatwa Group of Hospitals': {
        'type': 'Major Referral Hospital',
        'staff_counts': {'physicians': 85, 'nurses': 220, 'technicians': 95, 'admin': 45, 'support': 120},
        'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU', 'Laboratory', 'Radiology', 'Cardiology', 'Neurology', 'Oncology', 'Pharmacy', 'Maternity', 'Orthopedics', 'Psychiatry', 'Dermatology']
    },
    'Sally Mugabe Central Hospital': {
        'type': 'Major Referral Hospital', 
        'staff_counts': {'physicians': 78, 'nurses': 200, 'technicians': 88, 'admin': 42, 'support': 110},
        'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU', 'Laboratory', 'Radiology', 'Cardiology', 'Neurology', 'Oncology', 'Pharmacy', 'Maternity', 'Orthopedics', 'Psychiatry']
    },
    'Mpilo Central Hospital': {
        'type': 'Major Referral Hospital',
        'staff_counts': {'physicians': 72, 'nurses': 185, 'technicians': 82, 'admin': 38, 'support': 105},
        'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU', 'Laboratory', 'Radiology', 'Cardiology', 'Neurology', 'Oncology', 'Pharmacy', 'Maternity', 'Orthopedics']
    },
    'United Bulawayo Hospitals': {
        'type': 'Major Referral Hospital',
        'staff_counts': {'physicians': 68, 'nurses': 175, 'technicians': 78, 'admin': 36, 'support': 95},
        'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU', 'Laboratory', 'Radiology', 'Cardiology', 'Neurology', 'Pharmacy', 'Maternity', 'Orthopedics']
    },
    
    # PROVINCIAL HOSPITALS (Medium)
    'Chitungwiza Central Hospital': {
        'type': 'Provincial Hospital',
        'staff_counts': {'physicians': 45, 'nurses': 125, 'technicians': 55, 'admin': 28, 'support': 70},
        'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU', 'Laboratory', 'Radiology', 'Pharmacy', 'Maternity', 'Orthopedics']
    },
    'Gweru Provincial Hospital': {
        'type': 'Provincial Hospital',
        'staff_counts': {'physicians': 38, 'nurses': 110, 'technicians': 48, 'admin': 24, 'support': 60},
        'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'Laboratory', 'Radiology', 'Pharmacy', 'Maternity']
    },
    'Bindura Provincial Hospital': {
        'type': 'Provincial Hospital',
        'staff_counts': {'physicians': 32, 'nurses': 95, 'technicians': 42, 'admin': 20, 'support': 50},
        'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'Laboratory', 'Radiology', 'Pharmacy', 'Maternity']
    },
    
    # MISSION HOSPITALS (Smaller)
    'Karanda Mission Hospital': {
        'type': 'Mission Hospital',
        'staff_counts': {'physicians': 18, 'nurses': 65, 'technicians': 25, 'admin': 12, 'support': 30},
        'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'Laboratory', 'Pharmacy', 'Maternity']
    },
    
    # TEST HOSPITAL (Small)
    'Test Hospital for ML Demo': {
        'type': 'Test Hospital',
        'staff_counts': {'physicians': 12, 'nurses': 35, 'technicians': 15, 'admin': 8, 'support': 18},
        'departments': ['Emergency', 'Internal Medicine', 'Laboratory', 'Pharmacy']
    }
}

hospitals = Hospital.objects.all()
print(f"📋 Found {hospitals.count()} hospitals")

staff_counter = 1
total_created = 0

for hospital in hospitals:
    hospital_name = hospital.name
    
    # Get configuration for this hospital
    if hospital_name in hospital_configurations:
        config = hospital_configurations[hospital_name]
    else:
        # Default configuration for unknown hospitals
        config = {
            'type': 'District Hospital',
            'staff_counts': {'physicians': 25, 'nurses': 80, 'technicians': 35, 'admin': 18, 'support': 40},
            'departments': ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'Laboratory', 'Pharmacy']
        }
    
    print(f"\n🏥 Creating staff for: {hospital_name}")
    print(f"   🏷️ Type: {config['type']}")
    
    # Determine name set based on hospital location
    hospital_name_lower = hospital_name.lower()
    if any(word in hospital_name_lower for word in ['harare', 'sally mugabe', 'parirenyatwa', 'chitungwiza']):
        name_set = shona_names
        culture = "Shona"
    elif any(word in hospital_name_lower for word in ['bulawayo', 'mpilo', 'united bulawayo']):
        name_set = ndebele_names
        culture = "Ndebele"
    else:
        # Mix both for other hospitals
        name_set = {
            'physicians': shona_names['physicians'][:25] + ndebele_names['physicians'][:25],
            'nurses': shona_names['nurses'][:35] + ndebele_names['nurses'][:35],
            'technicians': shona_names['technicians'][:15] + ndebele_names['technicians'][:15],
            'admin': shona_names['admin'][:10] + ndebele_names['admin'][:10],
            'support': shona_names['support'][:12] + ndebele_names['support'][:12]
        }
        culture = "Mixed"
    
    print(f"   🌍 Using {culture} names")
    
    # Create departments based on hospital configuration
    departments = []
    for dept_name in config['departments']:
        dept, _ = Department.objects.get_or_create(
            hospital=hospital,
            name=dept_name,
            defaults={'description': f'{dept_name} department'}
        )
        departments.append(dept)
    
    # Create staff for each category with realistic numbers
    staff_data = [
        (categories['Physicians'], name_set['physicians'], config['staff_counts']['physicians']),
        (categories['Nurses'], name_set['nurses'], config['staff_counts']['nurses']),
        (categories['Technicians'], name_set['technicians'], config['staff_counts']['technicians']),
        (categories['Administrative Staff'], name_set['admin'], config['staff_counts']['admin']),
        (categories['Support Staff'], name_set['support'], config['staff_counts']['support']),
    ]
    
    hospital_staff_created = 0
    
    for category, names, count in staff_data:
        available_names = names.copy()
        random.shuffle(available_names)
        
        # Create multiple cycles of names if needed
        names_to_use = []
        cycles_needed = (count // len(available_names)) + 1
        for cycle in range(cycles_needed):
            for name in available_names:
                if len(names_to_use) < count:
                    # Add variation to repeated names
                    if cycle > 0:
                        base_name = name.split(' ', 1)[1] if ' ' in name else name
                        prefix = name.split(' ')[0]
                        names_to_use.append(f"{prefix} {base_name}")
                    else:
                        names_to_use.append(name)
        
        for i in range(count):
            name = names_to_use[i] if i < len(names_to_use) else f"Staff Member {i+1}"
            department = random.choice(departments)
            
            staff = Staff.objects.create(
                hospital=hospital,
                department=department,
                category=category,
                staff_id=f'STF-{hospital.id:02d}-{staff_counter:04d}',
                full_name=name,
                position='Staff Member',
                contact_number=f'+263{random.randint(700000000, 799999999)}',
                email=f"{name.lower().replace('dr. ', '').replace('sister ', '').replace('nurse ', '').replace('tech. ', '').replace('admin. ', '').replace('support. ', '').replace(' ', '.')}@{hospital.name.lower().replace(' ', '').replace('hospital', '').replace('group', '').replace('of', '')[:10]}.co.zw",
                is_active=True
            )
            
            staff_counter += 1
            total_created += 1
            hospital_staff_created += 1
        
        print(f"   ✅ Created {count} {category.name}")
    
    print(f"   📊 Total for {hospital_name}: {hospital_staff_created} staff members")

print(f"\n🎉 Successfully created {total_created} diverse staff members with realistic distribution!")

# Show final summary
print("\n📋 Final Staff Summary by Hospital:")
for hospital in hospitals:
    staff_by_category = {}
    total_hospital_staff = 0
    for staff in Staff.objects.filter(hospital=hospital):
        category = staff.category.name
        if category not in staff_by_category:
            staff_by_category[category] = 0
        staff_by_category[category] += 1
        total_hospital_staff += 1
    
    hospital_type = hospital_configurations.get(hospital.name, {}).get('type', 'District Hospital')
    print(f"\n🏥 {hospital.name} ({hospital_type}) - Total: {total_hospital_staff}")
    for category, count in staff_by_category.items():
        print(f"   - {category}: {count}")

print("\n✅ Database updated with realistic staff distribution!")
