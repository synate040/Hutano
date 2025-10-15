"""
Script to update hospital information in the HUTANO system.
Run this script directly:
python update_hospitals_shell.py
"""
import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

# Import models after Django setup
from core.models import Hospital, Department

# Define Zimbabwean hospitals
zimbabwe_hospitals = [
    {
        'name': 'Parirenyatwa Group of Hospitals',
        'location': 'Harare, Zimbabwe',
        'district': 'Harare Urban District',
        'province': 'Harare Province',
        'type': 'Tertiary',
        'bed_capacity': 1800,
        'departments': ['Surgery', 'Medicine', 'Pediatrics', 'Obstetrics & Gynecology', 'Psychiatry', 'Ophthalmology', 'Orthopedics', 'Oncology'],
        'staff': random.randint(800, 1200),
        'current_patients': random.randint(1200, 1600)
    },
    {
        'name': 'Sally Mugabe Central Hospital',
        'location': 'Harare, Zimbabwe',
        'district': 'Harare Urban District',
        'province': 'Harare Province',
        'type': 'Tertiary',
        'bed_capacity': 1200,
        'departments': ['Surgery', 'Medicine', 'Pediatrics', 'Obstetrics & Gynecology', 'Psychiatry'],
        'staff': random.randint(600, 900),
        'current_patients': random.randint(800, 1000)
    },
    {
        'name': 'Mpilo Central Hospital',
        'location': 'Bulawayo, Zimbabwe',
        'district': 'Bulawayo Metropolitan District',
        'province': 'Bulawayo Province',
        'type': 'Tertiary',
        'bed_capacity': 1000,
        'departments': ['Surgery', 'Medicine', 'Pediatrics', 'Obstetrics & Gynecology', 'Psychiatry', 'Orthopedics'],
        'staff': random.randint(500, 800),
        'current_patients': random.randint(700, 900)
    },
    {
        'name': 'Chitungwiza Central Hospital',
        'location': 'Chitungwiza, Zimbabwe',
        'district': 'Chitungwiza District',
        'province': 'Harare Province',
        'type': 'Secondary',
        'bed_capacity': 500,
        'departments': ['Surgery', 'Medicine', 'Pediatrics', 'Obstetrics & Gynecology'],
        'staff': random.randint(300, 500),
        'current_patients': random.randint(350, 450)
    },
    {
        'name': 'United Bulawayo Hospitals',
        'location': 'Bulawayo, Zimbabwe',
        'district': 'Bulawayo Metropolitan District',
        'province': 'Bulawayo Province',
        'type': 'Tertiary',
        'bed_capacity': 800,
        'departments': ['Surgery', 'Medicine', 'Pediatrics', 'Obstetrics & Gynecology', 'Psychiatry'],
        'staff': random.randint(400, 700),
        'current_patients': random.randint(600, 750)
    },
    {
        'name': 'Gweru Provincial Hospital',
        'location': 'Gweru, Zimbabwe',
        'district': 'Gweru District',
        'province': 'Midlands Province',
        'type': 'Secondary',
        'bed_capacity': 400,
        'departments': ['Surgery', 'Medicine', 'Pediatrics', 'Obstetrics & Gynecology'],
        'staff': random.randint(200, 350),
        'current_patients': random.randint(250, 350)
    },
    {
        'name': 'Bindura Provincial Hospital',
        'location': 'Bindura, Zimbabwe',
        'district': 'Bindura District',
        'province': 'Mashonaland Central Province',
        'type': 'Secondary',
        'bed_capacity': 300,
        'departments': ['Surgery', 'Medicine', 'Pediatrics', 'Obstetrics & Gynecology'],
        'staff': random.randint(150, 250),
        'current_patients': random.randint(200, 280)
    },
    {
        'name': 'Karanda Mission Hospital',
        'location': 'Mt Darwin, Zimbabwe',
        'district': 'Mt Darwin District',
        'province': 'Mashonaland Central Province',
        'type': 'Mission',
        'bed_capacity': 150,
        'departments': ['Surgery', 'Medicine', 'Pediatrics', 'Obstetrics & Gynecology'],
        'staff': random.randint(100, 180),
        'current_patients': random.randint(120, 140)
    }
]

def update_hospitals():
    """Update hospital information in the database."""
    print("Updating hospital information...")

    # Clear existing hospitals
    Hospital.objects.all().delete()
    print("Cleared existing hospitals")

    # Add new hospitals
    for i, hospital_data in enumerate(zimbabwe_hospitals, 1):
        # Create hospital
        is_rural = 'Mission' in hospital_data['type'] or 'Secondary' in hospital_data['type']
        hospital = Hospital.objects.create(
            name=hospital_data['name'],
            location=hospital_data['location'],
            district=hospital_data['district'],
            province=hospital_data['province'],
            bed_capacity=hospital_data['bed_capacity'],
            is_rural=is_rural
        )

        # Create departments
        for dept_name in hospital_data['departments']:
            Department.objects.create(
                name=dept_name,
                hospital=hospital
            )

        print(f"Added hospital: {hospital.name} with {len(hospital_data['departments'])} departments")

    print(f"Successfully added {len(zimbabwe_hospitals)} Zimbabwean hospitals")

if __name__ == "__main__":
    update_hospitals()
