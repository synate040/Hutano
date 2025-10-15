#!/usr/bin/env python3
"""
HUTANO Complete Name Uniqueness Script
=====================================

This script ensures every staff member has a completely unique name by using
a systematic approach with numbered variations and unique combinations.

Usage:
    python create_completely_unique_names.py
"""

import os
import sys
import django
import random
import string

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff, StaffCategory, Department

class CompletelyUniqueNameGenerator:
    def __init__(self):
        # Base Shona names
        self.shona_base_names = [
            'Tendai', 'Chipo', 'Farai', 'Rumbidzai', 'Takudzwa', 'Nyasha', 'Blessing', 'Tatenda',
            'Fungai', 'Chengetai', 'Tapiwa', 'Vimbai', 'Munyaradzi', 'Chiedza', 'Tafadzwa', 'Ruvimbo',
            'Tichaona', 'Shuvai', 'Tinashe', 'Kudakwashe', 'Tsitsi', 'Panashe', 'Rutendo', 'Tinotenda',
            'Tapfuma', 'Chengeto', 'Tafara', 'Tonderai', 'Tapiwanashe', 'Chiedza', 'Tafadzwa', 'Chengetai'
        ]
        
        # Base Shona surnames
        self.shona_base_surnames = [
            'Mukamuri', 'Mutasa', 'Nyamande', 'Chigumira', 'Madziva', 'Chidzonga', 'Chivasa', 'Mapfumo',
            'Chigumadzi', 'Chinamasa', 'Chikwanha', 'Makoni', 'Chipere', 'Mutindi', 'Zimba', 'Soko',
            'Chuma', 'Chirwa', 'Mwanza', 'Tembo', 'Banda', 'Phiri', 'Gumbo', 'Mhlanga', 'Bhebhe',
            'Siziba', 'Mthembu', 'Tshuma', 'Ndlovu', 'Khumalo', 'Nkomo', 'Mpofu', 'Dube', 'Sibanda'
        ]
        
        # Base Ndebele names
        self.ndebele_base_names = [
            'Sipho', 'Nomsa', 'Thabo', 'Busisiwe', 'Mandla', 'Nokuthula', 'Sizani', 'Themba',
            'Nomthandazo', 'Bhekani', 'Siphiwe', 'Nkosana', 'Nomvula', 'Sabelo', 'Thandiwe', 'Mthokozisi',
            'Nomcebo', 'Siyabonga', 'Nompumelelo', 'Bongani', 'Sindisiwe', 'Nkululeko', 'Nomathemba', 'Sibongile',
            'Nothando', 'Simbarashe', 'Nomfundo', 'Sifiso', 'Nolwazi', 'Sizolwethu', 'Nomhle', 'Sakhile'
        ]
        
        # Base Ndebele surnames
        self.ndebele_base_surnames = [
            'Nyathi', 'Moyo', 'Sibanda', 'Dube', 'Ncube', 'Mpofu', 'Nkomo', 'Khumalo', 'Ndlovu', 'Tshuma',
            'Mthembu', 'Siziba', 'Bhebhe', 'Gumbo', 'Mhlanga', 'Banda', 'Phiri', 'Tembo', 'Chirwa', 'Mwanza',
            'Zimba', 'Soko', 'Chuma', 'Mutindi', 'Makoni', 'Chipere', 'Mukamuri', 'Chivasa', 'Mapfumo', 'Chigumira'
        ]
        
        # Professional titles
        self.titles = {
            'physicians': ['Dr.'],
            'nurses': ['Sister', 'Nurse'],
            'technicians': ['Tech.'],
            'administrative': ['Admin.', 'Mr.', 'Mrs.', 'Ms.']
        }
        
        # Track all used names globally
        self.all_used_names = set()

    def generate_unique_name_variations(self, base_first_names, base_surnames, culture, category, count_needed):
        """Generate completely unique name variations using systematic approach."""
        titles = self.titles.get(category, [''])
        unique_names = []
        
        # Strategy 1: Use base combinations
        for first_name in base_first_names:
            for surname in base_surnames:
                for title in titles:
                    if len(unique_names) >= count_needed:
                        break
                    
                    if title:
                        full_name = f"{title} {first_name} {surname}"
                    else:
                        full_name = f"{first_name} {surname}"
                    
                    if full_name not in self.all_used_names:
                        unique_names.append(full_name)
                        self.all_used_names.add(full_name)
                
                if len(unique_names) >= count_needed:
                    break
            if len(unique_names) >= count_needed:
                break
        
        # Strategy 2: Add middle initials
        if len(unique_names) < count_needed:
            for first_name in base_first_names:
                for surname in base_surnames:
                    for title in titles:
                        for letter in string.ascii_uppercase:
                            if len(unique_names) >= count_needed:
                                break
                            
                            if title:
                                full_name = f"{title} {letter}. {first_name} {surname}"
                            else:
                                full_name = f"{letter}. {first_name} {surname}"
                            
                            if full_name not in self.all_used_names:
                                unique_names.append(full_name)
                                self.all_used_names.add(full_name)
                        
                        if len(unique_names) >= count_needed:
                            break
                    if len(unique_names) >= count_needed:
                        break
                if len(unique_names) >= count_needed:
                    break
        
        # Strategy 3: Add numbered variations
        if len(unique_names) < count_needed:
            for first_name in base_first_names:
                for surname in base_surnames:
                    for title in titles:
                        for num in range(1, 100):
                            if len(unique_names) >= count_needed:
                                break
                            
                            if title:
                                full_name = f"{title} {first_name} {surname} {num}"
                            else:
                                full_name = f"{first_name} {surname} {num}"
                            
                            if full_name not in self.all_used_names:
                                unique_names.append(full_name)
                                self.all_used_names.add(full_name)
                        
                        if len(unique_names) >= count_needed:
                            break
                    if len(unique_names) >= count_needed:
                        break
                if len(unique_names) >= count_needed:
                    break
        
        # Strategy 4: Double middle initials
        if len(unique_names) < count_needed:
            for first_name in base_first_names:
                for surname in base_surnames:
                    for title in titles:
                        for letter1 in string.ascii_uppercase:
                            for letter2 in string.ascii_uppercase:
                                if len(unique_names) >= count_needed:
                                    break
                                
                                if title:
                                    full_name = f"{title} {letter1}. {letter2}. {first_name} {surname}"
                                else:
                                    full_name = f"{letter1}. {letter2}. {first_name} {surname}"
                                
                                if full_name not in self.all_used_names:
                                    unique_names.append(full_name)
                                    self.all_used_names.add(full_name)
                            
                            if len(unique_names) >= count_needed:
                                break
                        if len(unique_names) >= count_needed:
                            break
                    if len(unique_names) >= count_needed:
                        break
                if len(unique_names) >= count_needed:
                    break
        
        return unique_names[:count_needed]

    def get_culture_for_hospital(self, hospital_name):
        """Determine cultural naming convention based on hospital location."""
        hospital_name = hospital_name.lower()
        
        # Harare/Mashonaland hospitals - use Shona names
        if any(word in hospital_name for word in ['harare', 'sally mugabe', 'parirenyatwa', 'chitungwiza']):
            return 'shona'
        
        # Bulawayo/Matabeleland hospitals - use Ndebele names
        elif any(word in hospital_name for word in ['bulawayo', 'mpilo', 'united bulawayo']):
            return 'ndebele'
        
        # Other regions - alternate between cultures
        else:
            return random.choice(['shona', 'ndebele'])

    def regenerate_all_staff_names(self):
        """Regenerate all staff names with completely unique combinations."""
        print("🚀 Starting HUTANO Complete Name Uniqueness Generation")
        print("=" * 70)
        
        # Clear tracking set
        self.all_used_names.clear()
        
        hospitals = Hospital.objects.all()
        total_updated = 0
        
        for hospital in hospitals:
            print(f"\n🏥 Processing {hospital.name}")
            
            # Get culture for this hospital
            culture = self.get_culture_for_hospital(hospital.name)
            print(f"   🏷️ Using {culture.title()} names")
            
            # Get appropriate name pools
            if culture == 'shona':
                first_names = self.shona_base_names
                surnames = self.shona_base_surnames
            else:
                first_names = self.ndebele_base_names
                surnames = self.ndebele_base_surnames
            
            # Get all staff for this hospital
            staff_members = Staff.objects.filter(hospital=hospital)
            print(f"   👥 Found {staff_members.count()} staff members")
            
            # Group staff by category
            staff_by_category = {}
            for staff in staff_members:
                category_name = staff.category.name.lower()
                if category_name not in staff_by_category:
                    staff_by_category[category_name] = []
                staff_by_category[category_name].append(staff)
            
            # Generate unique names for each category
            hospital_updated = 0
            for category_name, staff_list in staff_by_category.items():
                # Map category names to our naming convention
                if 'physician' in category_name or 'doctor' in category_name:
                    name_category = 'physicians'
                elif 'nurse' in category_name:
                    name_category = 'nurses'
                elif 'technician' in category_name or 'tech' in category_name:
                    name_category = 'technicians'
                else:
                    name_category = 'administrative'
                
                # Generate unique names for this category
                unique_names = self.generate_unique_name_variations(
                    first_names, surnames, culture, name_category, len(staff_list)
                )
                
                print(f"   📋 {category_name.title()}: {len(staff_list)} staff, {len(unique_names)} unique names generated")
                
                # Assign names to staff
                for i, staff in enumerate(staff_list):
                    if i < len(unique_names):
                        old_name = staff.full_name
                        new_name = unique_names[i]
                        
                        # Update staff name
                        staff.full_name = new_name
                        
                        # Update email to match new name
                        name_part = new_name.lower()
                        # Clean up the name for email
                        for title in ['dr. ', 'sister ', 'nurse ', 'tech. ', 'admin. ', 'mr. ', 'mrs. ', 'ms. ']:
                            name_part = name_part.replace(title, '')
                        name_part = name_part.replace(' ', '.').replace('..', '.')
                        
                        hospital_part = hospital.name.lower().replace(' ', '').replace('hospital', '').replace('group', '').replace('of', '')[:8]
                        staff.email = f"{name_part}@{hospital_part}.co.zw"
                        
                        staff.save()
                        
                        if i < 3:  # Show first 3 updates per category
                            print(f"   ✅ {old_name} → {new_name}")
                        
                        hospital_updated += 1
                        total_updated += 1
                    else:
                        print(f"   ⚠️  Could not generate unique name for {staff.full_name}")
            
            print(f"   📊 Updated {hospital_updated} staff names")
        
        print(f"\n🎉 Generation Complete!")
        print(f"📊 Total staff names updated: {total_updated}")
        print(f"🏥 Hospitals processed: {hospitals.count()}")
        print(f"🎯 Total unique names generated: {len(self.all_used_names)}")
        print("\n✨ Every staff member now has a completely unique name!")

if __name__ == "__main__":
    generator = CompletelyUniqueNameGenerator()
    generator.regenerate_all_staff_names()
