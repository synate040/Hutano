#!/usr/bin/env python3
"""
Simple script to update staff names with diverse Zimbabwean names
"""

import os
import sys
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff, StaffCategory, Department

def main():
    try:
        print("🔄 Updating staff names with diverse Zimbabwean names...")

        # Expanded Shona names for Harare hospitals
        shona_names = [
            'Dr. Tendai Mukamuri', 'Dr. Chipo Mutasa', 'Dr. Blessing Chikwanha',
            'Dr. Tarisai Moyo', 'Dr. Fungai Sibanda', 'Dr. Rutendo Ncube',
            'Dr. Takudzwa Mpofu', 'Dr. Nyasha Dube', 'Dr. Chengetai Ndlovu',
            'Dr. Tinashe Mujuru', 'Dr. Chiedza Makoni', 'Dr. Tafadzwa Gumbo',
            'Sister Chipo Nyathi', 'Nurse Tendai Nyathi', 'Sister Blessing Nyathi',
            'Nurse Rutendo Nyathi', 'Sister Nyasha Nyathi', 'Nurse Chiedza Nyathi',
            'Sister Tsitsi Nyathi', 'Nurse Rumbidzai Nyathi', 'Sister Rudo Nyathi',
            'Nurse Tarisai Nyathi', 'Sister Fungai Nyathi', 'Nurse Takudzwa Nyathi',
            'Sister Chengetai Nyathi', 'Nurse Tinashe Nyathi', 'Sister Munyaradzi Nyathi',
            'Nurse Farai Nyathi', 'Sister Tafadzwa Nyathi', 'Nurse Simba Nyathi',
            'Tech. Tendai Mukamuri', 'Tech. Blessing Chikwanha', 'Tech. Nyasha Mutasa',
            'Tech. Rutendo Moyo', 'Tech. Chipo Sibanda', 'Tech. Tarisai Ncube',
            'Tech. Fungai Mpofu', 'Tech. Chengetai Dube', 'Tech. Takudzwa Ndlovu',
            'Admin. Chipo Mukamuri', 'Admin. Tendai Chikwanha', 'Admin. Blessing Mutasa',
            'Admin. Nyasha Moyo', 'Admin. Rutendo Sibanda', 'Admin. Tarisai Ncube',
            'Support. Chipo Moyo', 'Support. Tendai Moyo', 'Support. Blessing Moyo',
            'Support. Nyasha Moyo', 'Support. Rutendo Moyo', 'Support. Tarisai Moyo'
        ]

        # Expanded Ndebele names for Bulawayo hospitals
        ndebele_names = [
            'Dr. Sipho Ncube', 'Dr. Nomsa Mpofu', 'Dr. Thabo Dube',
            'Dr. Busisiwe Ndlovu', 'Dr. Mandla Sibanda', 'Dr. Nokuthula Moyo',
            'Dr. Sizani Nkomo', 'Dr. Themba Khumalo', 'Dr. Nomthandazo Mthembu',
            'Dr. Bhekani Nyathi', 'Dr. Sithabile Tshuma', 'Dr. Mthokozisi Mlilo',
            'Sister Nomsa Nyathi', 'Nurse Sipho Nyathi', 'Sister Busisiwe Nyathi',
            'Nurse Thabo Nyathi', 'Sister Mandla Nyathi', 'Nurse Nokuthula Nyathi',
            'Sister Sizani Nyathi', 'Nurse Themba Nyathi', 'Sister Nomthandazo Nyathi',
            'Nurse Bhekani Nyathi', 'Sister Sithabile Nyathi', 'Nurse Mthokozisi Nyathi',
            'Sister Nompumelelo Nyathi', 'Nurse Sabelo Nyathi', 'Sister Thandiwe Nyathi',
            'Nurse Nkosana Nyathi', 'Sister Sindisiwe Nyathi', 'Nurse Mduduzi Nyathi',
            'Tech. Sipho Ncube', 'Tech. Nomsa Mpofu', 'Tech. Thabo Dube',
            'Tech. Busisiwe Ndlovu', 'Tech. Mandla Sibanda', 'Tech. Nokuthula Moyo',
            'Tech. Sizani Nkomo', 'Tech. Themba Khumalo', 'Tech. Nomthandazo Mthembu',
            'Admin. Nomsa Ncube', 'Admin. Sipho Mpofu', 'Admin. Busisiwe Dube',
            'Admin. Thabo Ndlovu', 'Admin. Mandla Sibanda', 'Admin. Nokuthula Moyo',
            'Support. Nomsa Ncube', 'Support. Sipho Mpofu', 'Support. Busisiwe Dube',
            'Support. Thabo Ndlovu', 'Support. Mandla Sibanda', 'Support. Nokuthula Moyo'
        ]

        hospitals = Hospital.objects.all()
        print(f"Found {hospitals.count()} hospitals")

        if hospitals.count() == 0:
            print("❌ No hospitals found in database!")
            return

        total_updated = 0

        for hospital in hospitals:
            print(f"\n🏥 Updating staff for: {hospital.name}")

            # Choose name set based on hospital location
            hospital_name_lower = hospital.name.lower()
            if any(word in hospital_name_lower for word in ['harare', 'sally mugabe', 'parirenyatwa', 'chitungwiza']):
                names = shona_names
                culture = "Shona"
            elif any(word in hospital_name_lower for word in ['bulawayo', 'mpilo', 'united bulawayo']):
                names = ndebele_names
                culture = "Ndebele"
            else:
                names = shona_names + ndebele_names  # Mix for other hospitals
                culture = "Mixed"

            print(f"   Using {culture} names")

            staff_members = Staff.objects.filter(hospital=hospital)
            print(f"   Found {staff_members.count()} staff members")

            if staff_members.count() == 0:
                print("   ⚠️ No staff found for this hospital")
                continue

            available_names = names.copy()
            random.shuffle(available_names)

            for i, staff in enumerate(staff_members):
                if i < len(available_names):
                    old_name = staff.full_name
                    new_name = available_names[i]
                    staff.full_name = new_name
                    staff.save()

                    print(f"   ✅ {old_name} → {new_name}")
                    total_updated += 1
                else:
                    print(f"   ⚠️ Ran out of names for staff member: {staff.full_name}")

        print(f"\n🎉 Successfully updated {total_updated} staff names!")

        # Show final summary
        print("\n📋 Staff Summary by Hospital:")
        for hospital in hospitals:
            staff_count = Staff.objects.filter(hospital=hospital).count()
            print(f"   {hospital.name}: {staff_count} staff members")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
