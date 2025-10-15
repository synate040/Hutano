import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff, StaffCategory, Department

print("🔄 Adding diverse staff names to database...")

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
        'Dr. Trust Moyo', 'Dr. Courage Sibanda', 'Dr. Prosper Ncube', 'Dr. Success Mpofu'
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
        'Sister Trust Nyathi', 'Nurse Courage Nyathi', 'Sister Prosper Nyathi', 'Nurse Success Nyathi'
    ],
    'technicians': [
        'Tech. Tendai Mukamuri', 'Tech. Blessing Chikwanha', 'Tech. Nyasha Mutasa', 'Tech. Rutendo Moyo',
        'Tech. Chipo Sibanda', 'Tech. Tarisai Ncube', 'Tech. Fungai Mpofu', 'Tech. Chengetai Dube',
        'Tech. Takudzwa Ndlovu', 'Tech. Chiedza Mujuru', 'Tech. Tsitsi Makoni', 'Tech. Rumbidzai Gumbo',
        'Tech. Tinashe Chigumira', 'Tech. Rudo Mapfumo', 'Tech. Munyaradzi Chidzonga', 'Tech. Farai Mukamuri',
        'Tech. Tafadzwa Chikwanha', 'Tech. Simba Mutasa', 'Tech. Patience Mukamuri', 'Tech. Memory Chikwanha'
    ],
    'admin': [
        'Admin. Chipo Mukamuri', 'Admin. Tendai Chikwanha', 'Admin. Blessing Mutasa', 'Admin. Nyasha Moyo',
        'Admin. Rutendo Sibanda', 'Admin. Tarisai Ncube', 'Admin. Fungai Mpofu', 'Admin. Chengetai Dube',
        'Admin. Chiedza Ndlovu', 'Admin. Takudzwa Mujuru', 'Admin. Tsitsi Makoni', 'Admin. Rumbidzai Gumbo'
    ],
    'support': [
        'Support. Chipo Moyo', 'Support. Tendai Moyo', 'Support. Blessing Moyo', 'Support. Nyasha Moyo',
        'Support. Rutendo Moyo', 'Support. Tarisai Moyo', 'Support. Fungai Moyo', 'Support. Chengetai Moyo',
        'Support. Chiedza Moyo', 'Support. Takudzwa Moyo', 'Support. Tsitsi Moyo', 'Support. Rumbidzai Moyo'
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
        'Sister Nomsa Ncube', 'Nurse Sipho Ncube', 'Sister Busisiwe Ncube', 'Nurse Thabo Ncube'
    ],
    'technicians': [
        'Tech. Sipho Ncube', 'Tech. Nomsa Mpofu', 'Tech. Thabo Dube', 'Tech. Busisiwe Ndlovu',
        'Tech. Mandla Sibanda', 'Tech. Nokuthula Moyo', 'Tech. Sizani Nkomo', 'Tech. Themba Khumalo',
        'Tech. Nomthandazo Mthembu', 'Tech. Bhekani Nyathi', 'Tech. Sithabile Tshuma', 'Tech. Mthokozisi Mlilo',
        'Tech. Nompumelelo Ngwenya', 'Tech. Sabelo Masuku', 'Tech. Thandiwe Mhlanga', 'Tech. Nkosana Ndiweni',
        'Tech. Sindisiwe Nkala', 'Tech. Mduduzi Gumede', 'Tech. Nomsa Nyathi', 'Tech. Sipho Nyathi'
    ],
    'admin': [
        'Admin. Nomsa Ncube', 'Admin. Sipho Mpofu', 'Admin. Busisiwe Dube', 'Admin. Thabo Ndlovu',
        'Admin. Mandla Sibanda', 'Admin. Nokuthula Moyo', 'Admin. Sizani Nkomo', 'Admin. Themba Khumalo',
        'Admin. Nomthandazo Mthembu', 'Admin. Bhekani Nyathi', 'Admin. Sithabile Tshuma', 'Admin. Mthokozisi Mlilo'
    ],
    'support': [
        'Support. Nomsa Ncube', 'Support. Sipho Mpofu', 'Support. Busisiwe Dube', 'Support. Thabo Ndlovu',
        'Support. Mandla Sibanda', 'Support. Nokuthula Moyo', 'Support. Sizani Nkomo', 'Support. Themba Khumalo',
        'Support. Nomthandazo Mthembu', 'Support. Bhekani Nyathi', 'Support. Sithabile Tshuma', 'Support. Mthokozisi Mlilo'
    ]
}

hospitals = Hospital.objects.all()
print(f"📋 Found {hospitals.count()} hospitals")

staff_counter = 1
total_created = 0

for hospital in hospitals:
    print(f"\n🏥 Creating staff for: {hospital.name}")
    
    # Determine name set based on hospital location
    hospital_name_lower = hospital.name.lower()
    if any(word in hospital_name_lower for word in ['harare', 'sally mugabe', 'parirenyatwa', 'chitungwiza']):
        name_set = shona_names
        culture = "Shona"
    elif any(word in hospital_name_lower for word in ['bulawayo', 'mpilo', 'united bulawayo']):
        name_set = ndebele_names
        culture = "Ndebele"
    else:
        # Mix both for other hospitals
        name_set = {
            'physicians': shona_names['physicians'][:20] + ndebele_names['physicians'][:20],
            'nurses': shona_names['nurses'][:20] + ndebele_names['nurses'][:20],
            'technicians': shona_names['technicians'][:10] + ndebele_names['technicians'][:10],
            'admin': shona_names['admin'][:6] + ndebele_names['admin'][:6],
            'support': shona_names['support'][:6] + ndebele_names['support'][:6]
        }
        culture = "Mixed"
    
    print(f"   Using {culture} names")
    
    # Create departments
    departments = []
    dept_names = ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU', 'Laboratory', 'Radiology']
    for dept_name in dept_names:
        dept, _ = Department.objects.get_or_create(
            hospital=hospital,
            name=dept_name,
            defaults={'description': f'{dept_name} department'}
        )
        departments.append(dept)
    
    # Create staff for each category
    staff_data = [
        (categories['Physicians'], name_set['physicians'], 25),
        (categories['Nurses'], name_set['nurses'], 40),
        (categories['Technicians'], name_set['technicians'], 20),
        (categories['Administrative Staff'], name_set['admin'], 12),
        (categories['Support Staff'], name_set['support'], 12),
    ]
    
    hospital_staff_created = 0
    
    for category, names, count in staff_data:
        available_names = names.copy()
        random.shuffle(available_names)
        
        for i in range(min(count, len(available_names))):
            name = available_names[i]
            department = random.choice(departments)
            
            staff = Staff.objects.create(
                hospital=hospital,
                department=department,
                category=category,
                staff_id=f'STF-{hospital.id:02d}-{staff_counter:04d}',
                full_name=name,
                position='Staff Member',
                contact_number=f'+263{random.randint(700000000, 799999999)}',
                email=f"{name.lower().replace('dr. ', '').replace('sister ', '').replace('nurse ', '').replace('tech. ', '').replace('admin. ', '').replace('support. ', '').replace(' ', '.')}@hospital.co.zw",
                is_active=True
            )
            
            staff_counter += 1
            total_created += 1
            hospital_staff_created += 1
        
        print(f"   ✅ Created {min(count, len(available_names))} {category.name}")
    
    print(f"   📊 Total for {hospital.name}: {hospital_staff_created} staff members")

print(f"\n🎉 Successfully created {total_created} diverse staff members!")

# Show final summary
print("\n📋 Final Staff Summary by Hospital:")
for hospital in hospitals:
    staff_by_category = {}
    for staff in Staff.objects.filter(hospital=hospital):
        category = staff.category.name
        if category not in staff_by_category:
            staff_by_category[category] = 0
        staff_by_category[category] += 1
    
    print(f"\n🏥 {hospital.name}:")
    for category, count in staff_by_category.items():
        print(f"   - {category}: {count}")

print("\n✅ Database updated with diverse Zimbabwean staff names!")
