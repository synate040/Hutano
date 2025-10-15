#!/usr/bin/env python3
"""
HUTANO Simple Unique Names Script
================================

This script makes every staff member name unique by adding systematic variations.

Usage:
    python simple_unique_names.py
"""

import os
import sys
import django
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff

class SimpleUniqueNameGenerator:
    def __init__(self):
        # Track used names
        self.used_names = set()
        
        # Zimbabwean first names
        self.first_names = [
            # Shona names
            'Tendai', 'Chipo', 'Farai', 'Rumbidzai', 'Takudzwa', 'Nyasha', 'Blessing', 'Tatenda',
            'Fungai', 'Chengetai', 'Tapiwa', 'Vimbai', 'Munyaradzi', 'Chiedza', 'Tafadzwa', 'Ruvimbo',
            'Tichaona', 'Shuvai', 'Tinashe', 'Kudakwashe', 'Tsitsi', 'Panashe', 'Rutendo', 'Tinotenda',
            'Tapfuma', 'Chengeto', 'Tafara', 'Tonderai', 'Tapiwanashe', 'Chiedza', 'Tafadzwa', 'Chengetai',
            # Ndebele names
            'Sipho', 'Nomsa', 'Thabo', 'Busisiwe', 'Mandla', 'Nokuthula', 'Sizani', 'Themba',
            'Nomthandazo', 'Bhekani', 'Siphiwe', 'Nkosana', 'Nomvula', 'Sabelo', 'Thandiwe', 'Mthokozisi',
            'Nomcebo', 'Siyabonga', 'Nompumelelo', 'Bongani', 'Sindisiwe', 'Nkululeko', 'Nomathemba', 'Sibongile',
            'Nothando', 'Simbarashe', 'Nomfundo', 'Sifiso', 'Nolwazi', 'Sizolwethu', 'Nomhle', 'Sakhile'
        ]
        
        # Zimbabwean surnames
        self.surnames = [
            # Common Zimbabwean surnames
            'Mukamuri', 'Mutasa', 'Nyamande', 'Chigumira', 'Madziva', 'Chidzonga', 'Chivasa', 'Mapfumo',
            'Chigumadzi', 'Chinamasa', 'Chikwanha', 'Makoni', 'Chipere', 'Mutindi', 'Zimba', 'Soko',
            'Chuma', 'Chirwa', 'Mwanza', 'Tembo', 'Banda', 'Phiri', 'Gumbo', 'Mhlanga', 'Bhebhe',
            'Siziba', 'Mthembu', 'Tshuma', 'Ndlovu', 'Khumalo', 'Nkomo', 'Mpofu', 'Dube', 'Sibanda',
            'Nyathi', 'Moyo', 'Ncube', 'Masuku', 'Mlilo', 'Maphosa', 'Ngwenya', 'Mthethwa', 'Zulu',
            'Mthembu', 'Nkala', 'Mhlanga', 'Mthembu', 'Mthembu', 'Mthembu', 'Mthembu', 'Mthembu'
        ]

    def generate_unique_name(self, category_name):
        """Generate a unique name for a staff member."""
        # Get appropriate title
        if 'physician' in category_name.lower() or 'doctor' in category_name.lower():
            title = 'Dr.'
        elif 'nurse' in category_name.lower():
            title = random.choice(['Sister', 'Nurse'])
        elif 'technician' in category_name.lower():
            title = 'Tech.'
        else:
            title = random.choice(['Admin.', 'Mr.', 'Mrs.', 'Ms.'])
        
        # Try to generate a unique name
        attempts = 0
        max_attempts = 1000
        
        while attempts < max_attempts:
            first_name = random.choice(self.first_names)
            surname = random.choice(self.surnames)
            
            # Create variations to ensure uniqueness
            if attempts < 100:
                # First 100 attempts: basic names
                full_name = f"{title} {first_name} {surname}"
            elif attempts < 200:
                # Next 100: add middle initial
                middle_initial = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                full_name = f"{title} {first_name} {middle_initial}. {surname}"
            elif attempts < 300:
                # Next 100: add number
                number = random.randint(1, 99)
                full_name = f"{title} {first_name} {surname} {number}"
            elif attempts < 400:
                # Next 100: add two middle initials
                initial1 = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                initial2 = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                full_name = f"{title} {first_name} {initial1}. {initial2}. {surname}"
            else:
                # Remaining: combination of initials and numbers
                initial = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                number = random.randint(1, 999)
                full_name = f"{title} {first_name} {initial}. {surname} {number}"
            
            if full_name not in self.used_names:
                self.used_names.add(full_name)
                return full_name
            
            attempts += 1
        
        # Fallback: use timestamp-based unique name
        import time
        timestamp = str(int(time.time() * 1000))[-6:]
        full_name = f"{title} {first_name} {surname} {timestamp}"
        self.used_names.add(full_name)
        return full_name

    def update_all_staff_names(self):
        """Update all staff names to be completely unique."""
        print("🚀 Starting HUTANO Simple Unique Names Generation")
        print("=" * 60)
        
        hospitals = Hospital.objects.all()
        total_updated = 0
        
        for hospital in hospitals:
            print(f"\n🏥 Processing {hospital.name}")
            
            staff_members = Staff.objects.filter(hospital=hospital)
            print(f"   👥 Found {staff_members.count()} staff members")
            
            hospital_updated = 0
            for i, staff in enumerate(staff_members):
                old_name = staff.full_name
                new_name = self.generate_unique_name(staff.category.name)
                
                # Update staff name
                staff.full_name = new_name
                
                # Update email to match new name
                name_part = new_name.lower()
                # Clean up the name for email
                for title in ['dr. ', 'sister ', 'nurse ', 'tech. ', 'admin. ', 'mr. ', 'mrs. ', 'ms. ']:
                    name_part = name_part.replace(title, '')
                name_part = name_part.replace(' ', '.').replace('..', '.').strip('.')
                
                hospital_part = hospital.name.lower().replace(' ', '').replace('hospital', '').replace('group', '').replace('of', '')[:8]
                staff.email = f"{name_part}@{hospital_part}.co.zw"
                
                staff.save()
                
                if i < 5:  # Show first 5 updates per hospital
                    print(f"   ✅ {old_name} → {new_name}")
                elif i == 5:
                    print(f"   ... (updating remaining {staff_members.count() - 5} staff)")
                
                hospital_updated += 1
                total_updated += 1
            
            print(f"   📊 Updated {hospital_updated} staff names")
        
        print(f"\n🎉 Generation Complete!")
        print(f"📊 Total staff names updated: {total_updated}")
        print(f"🏥 Hospitals processed: {hospitals.count()}")
        print(f"🎯 Total unique names generated: {len(self.used_names)}")
        print("\n✨ Every staff member now has a completely unique name!")

if __name__ == "__main__":
    generator = SimpleUniqueNameGenerator()
    generator.update_all_staff_names()
