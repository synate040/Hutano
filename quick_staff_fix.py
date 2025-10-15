import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff, StaffCategory, Department
import random

# Clear existing staff
Staff.objects.all().delete()
print("Cleared existing staff")

# Create categories
categories = {}
for cat_name in ['Physicians', 'Nurses', 'Technicians', 'Administrative Staff', 'Support Staff', 'Specialists', 'Residents', 'Pharmacists']:
    categories[cat_name], _ = StaffCategory.objects.get_or_create(name=cat_name)

# COMPREHENSIVE SHONA NAMES (for Harare/Mashonaland hospitals)
shona_physicians = [
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
]

shona_nurses = [
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
    'Sister Chipo Mukamuri', 'Nurse Tendai Mukamuri', 'Sister Blessing Mukamuri', 'Nurse Rutendo Mukamuri',
    'Sister Nyasha Mukamuri', 'Nurse Chiedza Mukamuri', 'Sister Tsitsi Mukamuri', 'Nurse Rumbidzai Mukamuri',
    'Sister Rudo Mukamuri', 'Nurse Tarisai Mukamuri', 'Sister Fungai Mukamuri', 'Nurse Takudzwa Mukamuri',
    'Sister Chengetai Mukamuri', 'Nurse Tinashe Mukamuri', 'Sister Munyaradzi Mukamuri', 'Nurse Farai Mukamuri',
    'Sister Tafadzwa Mukamuri', 'Nurse Simba Mukamuri', 'Sister Patience Mukamuri', 'Nurse Memory Mukamuri',
    'Sister Clever Mukamuri', 'Nurse Precious Mukamuri', 'Sister Gift Mukamuri', 'Nurse Loveness Mukamuri',
    'Sister Godwin Mukamuri', 'Nurse Mercy Mukamuri', 'Sister Justice Mukamuri', 'Nurse Brighton Mukamuri',
    'Sister Gracious Mukamuri', 'Nurse Honest Mukamuri', 'Sister Perseverance Mukamuri', 'Nurse Wisdom Mukamuri'
]

shona_technicians = [
    'Tech. Tendai Mukamuri', 'Tech. Blessing Chikwanha', 'Tech. Nyasha Mutasa', 'Tech. Rutendo Moyo',
    'Tech. Chipo Sibanda', 'Tech. Tarisai Ncube', 'Tech. Fungai Mpofu', 'Tech. Chengetai Dube',
    'Tech. Takudzwa Ndlovu', 'Tech. Chiedza Mujuru', 'Tech. Tsitsi Makoni', 'Tech. Rumbidzai Gumbo',
    'Tech. Tinashe Chigumira', 'Tech. Rudo Mapfumo', 'Tech. Munyaradzi Chidzonga', 'Tech. Farai Mukamuri',
    'Tech. Tafadzwa Chikwanha', 'Tech. Simba Mutasa', 'Tech. Patience Mukamuri', 'Tech. Memory Chikwanha',
    'Tech. Clever Mutasa', 'Tech. Precious Moyo', 'Tech. Gift Sibanda', 'Tech. Loveness Ncube',
    'Tech. Godwin Mpofu', 'Tech. Mercy Dube', 'Tech. Justice Ndlovu', 'Tech. Brighton Mujuru',
    'Tech. Gracious Makoni', 'Tech. Honest Gumbo', 'Tech. Perseverance Chigumira', 'Tech. Wisdom Mapfumo',
    'Tech. Faith Chidzonga', 'Tech. Hope Mukamuri', 'Tech. Peace Chikwanha', 'Tech. Joy Mutasa',
    'Tech. Trust Moyo', 'Tech. Courage Sibanda', 'Tech. Prosper Ncube', 'Tech. Success Mpofu'
]

shona_admin = [
    'Admin. Chipo Mukamuri', 'Admin. Tendai Chikwanha', 'Admin. Blessing Mutasa', 'Admin. Nyasha Moyo',
    'Admin. Rutendo Sibanda', 'Admin. Tarisai Ncube', 'Admin. Fungai Mpofu', 'Admin. Chengetai Dube',
    'Admin. Chiedza Ndlovu', 'Admin. Takudzwa Mujuru', 'Admin. Tsitsi Makoni', 'Admin. Rumbidzai Gumbo',
    'Admin. Tinashe Chigumira', 'Admin. Rudo Mapfumo', 'Admin. Munyaradzi Chidzonga', 'Admin. Farai Mukamuri',
    'Admin. Tafadzwa Chikwanha', 'Admin. Simba Mutasa', 'Admin. Patience Mukamuri', 'Admin. Memory Chikwanha',
    'Admin. Clever Mutasa', 'Admin. Precious Moyo', 'Admin. Gift Sibanda', 'Admin. Loveness Ncube',
    'Admin. Godwin Mpofu', 'Admin. Mercy Dube', 'Admin. Justice Ndlovu', 'Admin. Brighton Mujuru',
    'Admin. Gracious Makoni', 'Admin. Honest Gumbo', 'Admin. Perseverance Chigumira', 'Admin. Wisdom Mapfumo'
]

shona_support = [
    'Support. Chipo Moyo', 'Support. Tendai Moyo', 'Support. Blessing Moyo', 'Support. Nyasha Moyo',
    'Support. Rutendo Moyo', 'Support. Tarisai Moyo', 'Support. Fungai Moyo', 'Support. Chengetai Moyo',
    'Support. Chiedza Moyo', 'Support. Takudzwa Moyo', 'Support. Tsitsi Moyo', 'Support. Rumbidzai Moyo',
    'Support. Tinashe Moyo', 'Support. Rudo Moyo', 'Support. Munyaradzi Moyo', 'Support. Farai Moyo',
    'Support. Tafadzwa Moyo', 'Support. Simba Moyo', 'Support. Patience Moyo', 'Support. Memory Moyo',
    'Support. Clever Moyo', 'Support. Precious Moyo', 'Support. Gift Moyo', 'Support. Loveness Moyo',
    'Support. Godwin Moyo', 'Support. Mercy Moyo', 'Support. Justice Moyo', 'Support. Brighton Moyo',
    'Support. Gracious Moyo', 'Support. Honest Moyo', 'Support. Perseverance Moyo', 'Support. Wisdom Moyo'
]

# COMPREHENSIVE NDEBELE NAMES (for Bulawayo/Matabeleland hospitals)
ndebele_physicians = [
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
]

ndebele_nurses = [
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
    'Sister Busisiwe Mpofu', 'Nurse Thabo Mpofu', 'Sister Mandla Mpofu', 'Nurse Nokuthula Mpofu',
    'Sister Sizani Mpofu', 'Nurse Themba Mpofu', 'Sister Nomthandazo Mpofu', 'Nurse Bhekani Mpofu'
]

ndebele_technicians = [
    'Tech. Sipho Ncube', 'Tech. Nomsa Mpofu', 'Tech. Thabo Dube', 'Tech. Busisiwe Ndlovu',
    'Tech. Mandla Sibanda', 'Tech. Nokuthula Moyo', 'Tech. Sizani Nkomo', 'Tech. Themba Khumalo',
    'Tech. Nomthandazo Mthembu', 'Tech. Bhekani Nyathi', 'Tech. Sithabile Tshuma', 'Tech. Mthokozisi Mlilo',
    'Tech. Nompumelelo Ngwenya', 'Tech. Sabelo Masuku', 'Tech. Thandiwe Mhlanga', 'Tech. Nkosana Ndiweni',
    'Tech. Sindisiwe Nkala', 'Tech. Mduduzi Gumede', 'Tech. Nomsa Nyathi', 'Tech. Sipho Nyathi',
    'Tech. Thabo Nyathi', 'Tech. Busisiwe Nyathi', 'Tech. Mandla Nyathi', 'Tech. Nokuthula Nyathi',
    'Tech. Sizani Nyathi', 'Tech. Themba Nyathi', 'Tech. Nomthandazo Nyathi', 'Tech. Bhekani Nyathi',
    'Tech. Sithabile Nyathi', 'Tech. Mthokozisi Nyathi', 'Tech. Nompumelelo Nyathi', 'Tech. Sabelo Nyathi',
    'Tech. Thandiwe Nyathi', 'Tech. Nkosana Nyathi', 'Tech. Sindisiwe Nyathi', 'Tech. Mduduzi Nyathi',
    'Tech. Nomsa Tshuma', 'Tech. Sipho Tshuma', 'Tech. Thabo Tshuma', 'Tech. Busisiwe Tshuma'
]

ndebele_admin = [
    'Admin. Nomsa Ncube', 'Admin. Sipho Mpofu', 'Admin. Busisiwe Dube', 'Admin. Thabo Ndlovu',
    'Admin. Mandla Sibanda', 'Admin. Nokuthula Moyo', 'Admin. Sizani Nkomo', 'Admin. Themba Khumalo',
    'Admin. Nomthandazo Mthembu', 'Admin. Bhekani Nyathi', 'Admin. Sithabile Tshuma', 'Admin. Mthokozisi Mlilo',
    'Admin. Nompumelelo Ngwenya', 'Admin. Sabelo Masuku', 'Admin. Thandiwe Mhlanga', 'Admin. Nkosana Ndiweni',
    'Admin. Sindisiwe Nkala', 'Admin. Mduduzi Gumede', 'Admin. Nomsa Nyathi', 'Admin. Sipho Nyathi',
    'Admin. Thabo Nyathi', 'Admin. Busisiwe Nyathi', 'Admin. Mandla Nyathi', 'Admin. Nokuthula Nyathi',
    'Admin. Sizani Nyathi', 'Admin. Themba Nyathi', 'Admin. Nomthandazo Nyathi', 'Admin. Bhekani Nyathi',
    'Admin. Sithabile Nyathi', 'Admin. Mthokozisi Nyathi', 'Admin. Nompumelelo Nyathi', 'Admin. Sabelo Nyathi'
]

ndebele_support = [
    'Support. Nomsa Ncube', 'Support. Sipho Mpofu', 'Support. Busisiwe Dube', 'Support. Thabo Ndlovu',
    'Support. Mandla Sibanda', 'Support. Nokuthula Moyo', 'Support. Sizani Nkomo', 'Support. Themba Khumalo',
    'Support. Nomthandazo Mthembu', 'Support. Bhekani Nyathi', 'Support. Sithabile Tshuma', 'Support. Mthokozisi Mlilo',
    'Support. Nompumelelo Ngwenya', 'Support. Sabelo Masuku', 'Support. Thandiwe Mhlanga', 'Support. Nkosana Ndiweni',
    'Support. Sindisiwe Nkala', 'Support. Mduduzi Gumede', 'Support. Nomsa Nyathi', 'Support. Sipho Nyathi',
    'Support. Thabo Nyathi', 'Support. Busisiwe Nyathi', 'Support. Mandla Nyathi', 'Support. Nokuthula Nyathi',
    'Support. Sizani Nyathi', 'Support. Themba Nyathi', 'Support. Nomthandazo Nyathi', 'Support. Bhekani Nyathi',
    'Support. Sithabile Nyathi', 'Support. Mthokozisi Nyathi', 'Support. Nompumelelo Nyathi', 'Support. Sabelo Nyathi'
]

hospitals = Hospital.objects.all()
print(f"Found {hospitals.count()} hospitals")

staff_counter = 1
total_created = 0

for hospital in hospitals:
    print(f"Creating staff for: {hospital.name}")

    # Determine name set based on hospital location
    hospital_name_lower = hospital.name.lower()
    if any(word in hospital_name_lower for word in ['harare', 'sally mugabe', 'parirenyatwa', 'chitungwiza']):
        physicians = shona_physicians
        nurses = shona_nurses
        technicians = shona_technicians
        admin = shona_admin
        support = shona_support
        culture = "Shona"
    elif any(word in hospital_name_lower for word in ['bulawayo', 'mpilo', 'united bulawayo']):
        physicians = ndebele_physicians
        nurses = ndebele_nurses
        technicians = ndebele_technicians
        admin = ndebele_admin
        support = ndebele_support
        culture = "Ndebele"
    else:
        # Mix both for other hospitals
        physicians = shona_physicians[:20] + ndebele_physicians[:20]
        nurses = shona_nurses[:30] + ndebele_nurses[:30]
        technicians = shona_technicians[:20] + ndebele_technicians[:20]
        admin = shona_admin[:16] + ndebele_admin[:16]
        support = shona_support[:16] + ndebele_support[:16]
        culture = "Mixed"

    print(f"   Using {culture} names")

    # Create multiple departments for variety
    departments = []
    dept_names = ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU', 'Laboratory', 'Radiology', 'Pharmacy', 'Maternity', 'Oncology']
    for dept_name in dept_names:
        dept, _ = Department.objects.get_or_create(
            hospital=hospital,
            name=dept_name,
            defaults={'description': f'{dept_name} department'}
        )
        departments.append(dept)

    # Create staff for each category with large numbers
    staff_data = [
        (categories['Physicians'], physicians, 50, ['Senior Consultant', 'Specialist', 'Consultant', 'Registrar', 'Junior Doctor']),
        (categories['Nurses'], nurses, 150, ['Senior Nurse', 'Staff Nurse', 'Charge Nurse', 'Ward Sister', 'Clinical Nurse']),
        (categories['Technicians'], technicians, 80, ['Senior Technician', 'Lab Technician', 'Radiographer', 'Biomedical Engineer']),
        (categories['Administrative Staff'], admin, 50, ['Administrator', 'Clerk', 'Secretary', 'Coordinator', 'Manager']),
        (categories['Support Staff'], support, 100, ['Cleaner', 'Security Guard', 'Porter', 'Maintenance', 'Kitchen Staff']),
    ]

    hospital_staff_created = 0

    for category, names, count, positions in staff_data:
        available_names = names.copy()
        random.shuffle(available_names)

        for i in range(min(count, len(available_names))):
            name = available_names[i]
            department = random.choice(departments)
            position = random.choice(positions)

            staff = Staff.objects.create(
                hospital=hospital,
                department=department,
                category=category,
                staff_id=f'STF-{hospital.id:02d}-{staff_counter:04d}',
                full_name=name,
                position=position,
                contact_number=f'+263{random.randint(700000000, 799999999)}',
                email=f"{name.lower().replace('dr. ', '').replace('sister ', '').replace('nurse ', '').replace('tech. ', '').replace('admin. ', '').replace('support. ', '').replace(' ', '.')}@{hospital.name.lower().replace(' ', '').replace('hospital', '').replace('group', '').replace('of', '')[:10]}.co.zw",
                is_active=True
            )

            staff_counter += 1
            total_created += 1
            hospital_staff_created += 1

        print(f"   ✅ Created {min(count, len(available_names))} {category.name}")

    print(f"  📊 Total created for {hospital.name}: {hospital_staff_created} staff members")

print(f"Successfully created {total_created} diverse staff members!")

# Show summary
for hospital in hospitals:
    staff_by_category = {}
    for staff in Staff.objects.filter(hospital=hospital):
        category = staff.category.name
        if category not in staff_by_category:
            staff_by_category[category] = 0
        staff_by_category[category] += 1

    print(f"\n{hospital.name}:")
    for category, count in staff_by_category.items():
        print(f"  - {category}: {count}")
