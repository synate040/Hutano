#!/usr/bin/env python3
"""
Update HUTANO Staff Names with Diverse Shona and Ndebele Names

This script updates staff names in the database to use authentic Zimbabwean names
distributed across different hospitals to reflect the cultural diversity.
"""

import os
import sys
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, Staff, StaffCategory


class StaffNameUpdater:
    """Updates staff names with authentic Zimbabwean names."""
    
    def __init__(self):
        # Shona names (predominantly for Harare/Mashonaland hospitals)
        self.shona_names = {
            'physicians': [
                'Dr. Tendai Mukamuri', 'Dr. Chipo Mutasa', 'Dr. Blessing Chikwanha',
                'Dr. Tarisai Moyo', 'Dr. Fungai Sibanda', 'Dr. Rutendo Ncube',
                'Dr. Takudzwa Mpofu', 'Dr. Nyasha Dube', 'Dr. Chengetai Ndlovu',
                'Dr. Tinashe Mujuru', 'Dr. Chiedza Makoni', 'Dr. Tafadzwa Gumbo',
                'Dr. Rumbidzai Chigumira', 'Dr. Munyaradzi Mapfumo', 'Dr. Tsitsi Chidzonga',
                'Dr. Farai Mukamuri', 'Dr. Rudo Chikwanha', 'Dr. Simba Mutasa'
            ],
            'nurses': [
                'Sister Chipo Mukamuri', 'Nurse Tendai Chikwanha', 'Sister Blessing Mutasa',
                'Nurse Rutendo Moyo', 'Sister Nyasha Sibanda', 'Nurse Chiedza Ncube',
                'Sister Tsitsi Mpofu', 'Nurse Rumbidzai Dube', 'Sister Rudo Ndlovu',
                'Nurse Tarisai Mujuru', 'Sister Fungai Makoni', 'Nurse Takudzwa Gumbo',
                'Sister Chengetai Chigumira', 'Nurse Tinashe Mapfumo', 'Sister Munyaradzi Chidzonga',
                'Nurse Farai Mukamuri', 'Sister Tafadzwa Chikwanha', 'Nurse Simba Mutasa'
            ],
            'technicians': [
                'Tech. Tendai Mukamuri', 'Tech. Blessing Chikwanha', 'Tech. Nyasha Mutasa',
                'Tech. Rutendo Moyo', 'Tech. Chipo Sibanda', 'Tech. Tarisai Ncube',
                'Tech. Fungai Mpofu', 'Tech. Chengetai Dube', 'Tech. Takudzwa Ndlovu',
                'Tech. Chiedza Mujuru', 'Tech. Tsitsi Makoni', 'Tech. Rumbidzai Gumbo',
                'Tech. Tinashe Chigumira', 'Tech. Rudo Mapfumo', 'Tech. Munyaradzi Chidzonga',
                'Tech. Farai Mukamuri', 'Tech. Tafadzwa Chikwanha', 'Tech. Simba Mutasa'
            ],
            'administrative': [
                'Admin. Chipo Mukamuri', 'Admin. Tendai Chikwanha', 'Admin. Blessing Mutasa',
                'Admin. Nyasha Moyo', 'Admin. Rutendo Sibanda', 'Admin. Tarisai Ncube',
                'Admin. Fungai Mpofu', 'Admin. Chengetai Dube', 'Admin. Chiedza Ndlovu',
                'Admin. Takudzwa Mujuru', 'Admin. Tsitsi Makoni', 'Admin. Rumbidzai Gumbo',
                'Admin. Tinashe Chigumira', 'Admin. Rudo Mapfumo', 'Admin. Munyaradzi Chidzonga',
                'Admin. Farai Mukamuri', 'Admin. Tafadzwa Chikwanha', 'Admin. Simba Mutasa'
            ]
        }
        
        # Ndebele names (predominantly for Bulawayo/Matabeleland hospitals)
        self.ndebele_names = {
            'physicians': [
                'Dr. Sipho Ncube', 'Dr. Nomsa Mpofu', 'Dr. Thabo Dube',
                'Dr. Busisiwe Ndlovu', 'Dr. Mandla Sibanda', 'Dr. Nokuthula Moyo',
                'Dr. Sizani Nkomo', 'Dr. Themba Khumalo', 'Dr. Nomthandazo Mthembu',
                'Dr. Bhekani Nyathi', 'Dr. Sithabile Tshuma', 'Dr. Mthokozisi Mlilo',
                'Dr. Nompumelelo Ngwenya', 'Dr. Sabelo Masuku', 'Dr. Thandiwe Mhlanga',
                'Dr. Nkosana Ndiweni', 'Dr. Sindisiwe Nkala', 'Dr. Mduduzi Gumede'
            ],
            'nurses': [
                'Sister Nomsa Ncube', 'Nurse Sipho Mpofu', 'Sister Busisiwe Dube',
                'Nurse Thabo Ndlovu', 'Sister Mandla Sibanda', 'Nurse Nokuthula Moyo',
                'Sister Sizani Nkomo', 'Nurse Themba Khumalo', 'Sister Nomthandazo Mthembu',
                'Nurse Bhekani Nyathi', 'Sister Sithabile Tshuma', 'Nurse Mthokozisi Mlilo',
                'Sister Nompumelelo Ngwenya', 'Nurse Sabelo Masuku', 'Sister Thandiwe Mhlanga',
                'Nurse Nkosana Ndiweni', 'Sister Sindisiwe Nkala', 'Nurse Mduduzi Gumede'
            ],
            'technicians': [
                'Tech. Sipho Ncube', 'Tech. Nomsa Mpofu', 'Tech. Thabo Dube',
                'Tech. Busisiwe Ndlovu', 'Tech. Mandla Sibanda', 'Tech. Nokuthula Moyo',
                'Tech. Sizani Nkomo', 'Tech. Themba Khumalo', 'Tech. Nomthandazo Mthembu',
                'Tech. Bhekani Nyathi', 'Tech. Sithabile Tshuma', 'Tech. Mthokozisi Mlilo',
                'Tech. Nompumelelo Ngwenya', 'Tech. Sabelo Masuku', 'Tech. Thandiwe Mhlanga',
                'Tech. Nkosana Ndiweni', 'Tech. Sindisiwe Nkala', 'Tech. Mduduzi Gumede'
            ],
            'administrative': [
                'Admin. Nomsa Ncube', 'Admin. Sipho Mpofu', 'Admin. Busisiwe Dube',
                'Admin. Thabo Ndlovu', 'Admin. Mandla Sibanda', 'Admin. Nokuthula Moyo',
                'Admin. Sizani Nkomo', 'Admin. Themba Khumalo', 'Admin. Nomthandazo Mthembu',
                'Admin. Bhekani Nyathi', 'Admin. Sithabile Tshuma', 'Admin. Mthokozisi Mlilo',
                'Admin. Nompumelelo Ngwenya', 'Admin. Sabelo Masuku', 'Admin. Thandiwe Mhlanga',
                'Admin. Nkosana Ndiweni', 'Admin. Sindisiwe Nkala', 'Admin. Mduduzi Gumede'
            ]
        }
        
        # Mixed names for other regions
        self.mixed_names = {
            'physicians': [
                'Dr. Patience Chigumira', 'Dr. Brighton Mapfumo', 'Dr. Memory Chidzonga',
                'Dr. Clever Mukamuri', 'Dr. Precious Chikwanha', 'Dr. Gift Mutasa',
                'Dr. Loveness Moyo', 'Dr. Godwin Sibanda', 'Dr. Mercy Ncube',
                'Dr. Justice Mpofu', 'Dr. Grace Dube', 'Dr. Wisdom Ndlovu'
            ],
            'nurses': [
                'Sister Patience Chigumira', 'Nurse Brighton Mapfumo', 'Sister Memory Chidzonga',
                'Nurse Clever Mukamuri', 'Sister Precious Chikwanha', 'Nurse Gift Mutasa',
                'Sister Loveness Moyo', 'Nurse Godwin Sibanda', 'Sister Mercy Ncube',
                'Nurse Justice Mpofu', 'Sister Grace Dube', 'Nurse Wisdom Ndlovu'
            ],
            'technicians': [
                'Tech. Patience Chigumira', 'Tech. Brighton Mapfumo', 'Tech. Memory Chidzonga',
                'Tech. Clever Mukamuri', 'Tech. Precious Chikwanha', 'Tech. Gift Mutasa',
                'Tech. Loveness Moyo', 'Tech. Godwin Sibanda', 'Tech. Mercy Ncube',
                'Tech. Justice Mpofu', 'Tech. Grace Dube', 'Tech. Wisdom Ndlovu'
            ],
            'administrative': [
                'Admin. Patience Chigumira', 'Admin. Brighton Mapfumo', 'Admin. Memory Chidzonga',
                'Admin. Clever Mukamuri', 'Admin. Precious Chikwanha', 'Admin. Gift Mutasa',
                'Admin. Loveness Moyo', 'Admin. Godwin Sibanda', 'Admin. Mercy Ncube',
                'Admin. Justice Mpofu', 'Admin. Grace Dube', 'Admin. Wisdom Ndlovu'
            ]
        }
    
    def get_hospital_name_set(self, hospital_name):
        """Determine which name set to use based on hospital location."""
        hospital_name = hospital_name.lower()
        
        # Harare/Mashonaland hospitals - use Shona names
        if any(word in hospital_name for word in ['harare', 'sally mugabe', 'parirenyatwa', 'chitungwiza']):
            return self.shona_names
        
        # Bulawayo/Matabeleland hospitals - use Ndebele names
        elif any(word in hospital_name for word in ['bulawayo', 'mpilo', 'united bulawayo']):
            return self.ndebele_names
        
        # Other regions - use mixed names
        else:
            return self.mixed_names
    
    def get_staff_category_key(self, category_name):
        """Map staff category to name category."""
        category_name = category_name.lower()
        
        if 'physician' in category_name or 'doctor' in category_name:
            return 'physicians'
        elif 'nurse' in category_name:
            return 'nurses'
        elif 'technician' in category_name or 'tech' in category_name:
            return 'technicians'
        else:
            return 'administrative'
    
    def update_staff_names(self):
        """Update all staff names with appropriate cultural names."""
        print("🔄 Updating staff names with diverse Shona and Ndebele names...")
        
        hospitals = Hospital.objects.all()
        total_updated = 0
        
        for hospital in hospitals:
            print(f"\n🏥 Updating staff for: {hospital.name}")
            
            # Get appropriate name set for this hospital
            name_set = self.get_hospital_name_set(hospital.name)
            
            # Get all staff for this hospital
            staff_members = Staff.objects.filter(hospital=hospital)
            
            # Track used names to avoid duplicates within the same hospital
            used_names = set()
            
            for staff in staff_members:
                # Determine staff category
                category_key = self.get_staff_category_key(staff.category.name)
                
                # Get available names for this category
                available_names = [name for name in name_set[category_key] if name not in used_names]
                
                if available_names:
                    # Select a random name
                    new_name = random.choice(available_names)
                    used_names.add(new_name)
                    
                    # Update staff name
                    old_name = staff.full_name
                    staff.full_name = new_name
                    
                    # Update email to match new name
                    name_part = new_name.lower().replace('dr. ', '').replace('sister ', '').replace('nurse ', '').replace('tech. ', '').replace('admin. ', '').replace(' ', '.')
                    hospital_part = hospital.name.lower().replace(' ', '').replace('hospital', '').replace('group', '').replace('of', '')
                    staff.email = f"{name_part}@{hospital_part}.co.zw"
                    
                    staff.save()
                    
                    print(f"  ✅ Updated: {old_name} → {new_name}")
                    total_updated += 1
                else:
                    print(f"  ⚠️  No available names for {staff.full_name} ({category_key})")
        
        print(f"\n🎉 Successfully updated {total_updated} staff names!")
        return total_updated
    
    def generate_additional_staff(self, hospital, count_per_category=None):
        """Generate additional staff with diverse names for a specific hospital."""
        if count_per_category is None:
            count_per_category = {'physicians': 12, 'nurses': 36, 'technicians': 16, 'administrative': 8}
        
        print(f"\n➕ Generating additional staff for: {hospital.name}")
        
        # Get appropriate name set for this hospital
        name_set = self.get_hospital_name_set(hospital.name)
        
        # Get or create staff categories
        categories = {
            'physicians': StaffCategory.objects.get_or_create(name='Physicians')[0],
            'nurses': StaffCategory.objects.get_or_create(name='Nurses')[0],
            'technicians': StaffCategory.objects.get_or_create(name='Technicians')[0],
            'administrative': StaffCategory.objects.get_or_create(name='Administrative Staff')[0],
        }
        
        # Get hospital departments
        departments = list(hospital.departments.all())
        if not departments:
            print(f"  ⚠️  No departments found for {hospital.name}")
            return 0
        
        total_created = 0
        staff_counter = Staff.objects.filter(hospital=hospital).count() + 1
        
        for category_key, count in count_per_category.items():
            category = categories[category_key]
            available_names = name_set[category_key].copy()
            random.shuffle(available_names)
            
            for i in range(min(count, len(available_names))):
                name = available_names[i]
                department = random.choice(departments)
                
                # Create staff member
                staff = Staff.objects.create(
                    hospital=hospital,
                    department=department,
                    category=category,
                    staff_id=f'STF-{hospital.id:02d}-{staff_counter:04d}',
                    full_name=name,
                    position=self.get_position_for_category(category_key),
                    contact_number=f'+263{random.randint(700000000, 799999999)}',
                    email=f"{name.lower().replace('dr. ', '').replace('sister ', '').replace('nurse ', '').replace('tech. ', '').replace('admin. ', '').replace(' ', '.')}@{hospital.name.lower().replace(' ', '').replace('hospital', '').replace('group', '').replace('of', '')}.co.zw",
                    is_active=True
                )
                
                print(f"  ✅ Created: {name} ({category.name})")
                total_created += 1
                staff_counter += 1
        
        print(f"  📊 Created {total_created} new staff members")
        return total_created
    
    def get_position_for_category(self, category_key):
        """Get appropriate position title for staff category."""
        positions = {
            'physicians': ['Senior Consultant', 'Specialist', 'Consultant', 'Registrar'],
            'nurses': ['Senior Nurse', 'Staff Nurse', 'Charge Nurse', 'Clinical Nurse'],
            'technicians': ['Senior Technician', 'Technician', 'Lab Technician', 'Radiographer'],
            'administrative': ['Administrator', 'Clerk', 'Secretary', 'Coordinator']
        }
        return random.choice(positions[category_key])


def main():
    """Main function to update staff names."""
    updater = StaffNameUpdater()
    
    print("🏥 HUTANO Staff Name Diversification")
    print("=" * 50)
    
    # Check if we have hospitals
    hospitals = Hospital.objects.all()
    if not hospitals.exists():
        print("❌ No hospitals found. Please run hospital data setup first.")
        return
    
    print(f"Found {hospitals.count()} hospitals:")
    for hospital in hospitals:
        staff_count = Staff.objects.filter(hospital=hospital).count()
        print(f"  - {hospital.name}: {staff_count} staff members")
    
    # Update existing staff names
    updated_count = updater.update_staff_names()
    
    # Optionally generate additional staff for hospitals with few staff
    print("\n" + "=" * 50)
    print("🔍 Checking for hospitals needing additional staff...")
    
    for hospital in hospitals:
        staff_count = Staff.objects.filter(hospital=hospital).count()
        if staff_count < 50:  # If hospital has fewer than 50 staff
            print(f"\n{hospital.name} has only {staff_count} staff members.")
            response = input(f"Generate additional staff? (y/n): ").lower().strip()
            if response == 'y':
                updater.generate_additional_staff(hospital)
    
    print("\n🎉 Staff name diversification completed!")
    print(f"📊 Total staff updated: {updated_count}")
    
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
            print(f"  - {category}: {count}")


if __name__ == "__main__":
    main()
