#!/usr/bin/env python3
"""
HUTANO Simple Demo Data Generator
Creates focused, demonstration-ready data to highlight system capabilities
"""

import os
import django
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import (
    Hospital, Department, StaffCategory, Staff, PatientAdmission,
    DocumentUpload, DataInsight, PredictionComparison
)
from django.contrib.auth.models import User

def clear_demo_data():
    """Clear existing demo data safely."""
    print("🧹 Clearing existing demo data...")

    # Clear in small batches to avoid SQL variable limit
    try:
        # Clear patient admissions in batches
        while PatientAdmission.objects.exists():
            batch = PatientAdmission.objects.all()[:1000]
            batch_ids = list(batch.values_list('id', flat=True))
            PatientAdmission.objects.filter(id__in=batch_ids).delete()

        print("✅ Demo data cleared successfully")
    except Exception as e:
        print(f"⚠️  Warning: {e}")
        print("Continuing with data generation...")

def create_sample_csv_files():
    """Create sample CSV files for ML model demonstration."""
    print("\n📊 Creating sample CSV files for ML demonstration...")

    # Create sample data directory
    os.makedirs('sample_data', exist_ok=True)

    # 1. Hospital Admissions Data (Most Important for Demo)
    print("  📈 Creating hospital_admissions_demo.csv...")

    dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
    admissions_data = []

    for date in dates:
        # Base admissions with realistic patterns
        base_admissions = 45

        # Weekly pattern (Monday-Tuesday peak)
        day_of_week = date.weekday()
        if day_of_week in [0, 1]:  # Monday, Tuesday
            weekly_factor = random.uniform(1.3, 1.6)
        elif day_of_week in [5, 6]:  # Weekend
            weekly_factor = random.uniform(0.6, 0.8)
        else:
            weekly_factor = random.uniform(0.9, 1.2)

        # Seasonal pattern (rainy season peak)
        month = date.month
        if month in [11, 12, 1, 2]:  # Rainy season
            seasonal_factor = random.uniform(1.2, 1.5)
        elif month in [6, 7, 8]:  # Dry season
            seasonal_factor = random.uniform(0.8, 1.0)
        else:
            seasonal_factor = random.uniform(0.9, 1.1)

        # Random noise
        noise = random.uniform(0.8, 1.2)

        daily_admissions = int(base_admissions * weekly_factor * seasonal_factor * noise)
        emergency_admissions = int(daily_admissions * random.uniform(0.3, 0.7))

        admissions_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'admissions': daily_admissions,
            'emergency_admissions': emergency_admissions,
            'elective_admissions': daily_admissions - emergency_admissions,
            'bed_occupancy_rate': round(random.uniform(75, 95), 1),
            'average_length_of_stay': round(random.uniform(3.5, 7.2), 1),
            'staff_on_duty': random.randint(80, 120),
            'icu_admissions': random.randint(2, 8),
            'discharge_rate': round(random.uniform(0.8, 1.2), 2),
            'readmission_rate': round(random.uniform(0.05, 0.15), 2)
        })

    df_admissions = pd.DataFrame(admissions_data)
    df_admissions.to_csv('sample_data/hospital_admissions_demo.csv', index=False)

    # 2. Resource Utilization Data
    print("  🏥 Creating resource_utilization_demo.csv...")

    resource_data = []
    for date in dates:
        bed_capacity = 500
        beds_occupied = random.randint(350, 475)
        occupancy_rate = round((beds_occupied / bed_capacity) * 100, 1)

        resource_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'bed_capacity': bed_capacity,
            'beds_occupied': beds_occupied,
            'occupancy_rate': occupancy_rate,
            'icu_beds_total': 50,
            'icu_beds_occupied': random.randint(30, 48),
            'ventilators_total': 25,
            'ventilators_in_use': random.randint(10, 23),
            'oxygen_supply_level': round(random.uniform(85, 100), 1),
            'medication_stock_level': round(random.uniform(70, 95), 1),
            'staff_utilization_rate': round(random.uniform(80, 98), 1)
        })

    df_resources = pd.DataFrame(resource_data)
    df_resources.to_csv('sample_data/resource_utilization_demo.csv', index=False)

    # 3. Patient Demographics Data
    print("  👥 Creating patient_demographics_demo.csv...")

    # Zimbabwean names
    first_names = [
        'Tendai', 'Chipo', 'Blessing', 'Nyasha', 'Rutendo', 'Tarisai', 'Fungai', 'Chengetai',
        'Sipho', 'Nomsa', 'Thabo', 'Busisiwe', 'Mandla', 'Nokuthula', 'Sizani', 'Themba'
    ]

    surnames = [
        'Mukamuri', 'Mutasa', 'Chikwanha', 'Moyo', 'Sibanda', 'Ncube', 'Mpofu', 'Dube',
        'Ndlovu', 'Nyathi', 'Tshuma', 'Mlilo', 'Ngwenya', 'Masuku', 'Mhlanga', 'Gumbo'
    ]

    # Common diagnoses in Zimbabwe
    diagnoses = [
        'Malaria', 'Pneumonia', 'Tuberculosis', 'HIV/AIDS complications', 'Hypertension',
        'Diabetes complications', 'Gastroenteritis', 'Respiratory infections', 'Trauma',
        'Maternal complications', 'Malnutrition', 'Typhoid fever'
    ]

    demographics_data = []
    for i in range(500):  # 500 sample patients
        age = random.randint(0, 85)
        first_name = random.choice(first_names)
        surname = random.choice(surnames)

        # Age-based diagnosis probabilities
        if age < 5:
            diagnosis = random.choice(['Pneumonia', 'Malnutrition', 'Gastroenteritis', 'Malaria'])
        elif age < 18:
            diagnosis = random.choice(['Trauma', 'Respiratory infections', 'Gastroenteritis', 'Malaria'])
        elif age < 60:
            diagnosis = random.choice(['Trauma', 'Hypertension', 'Diabetes complications', 'Tuberculosis', 'HIV/AIDS complications'])
        else:
            diagnosis = random.choice(['Hypertension', 'Diabetes complications', 'Pneumonia', 'Respiratory infections'])

        demographics_data.append({
            'patient_id': f'PAT-{i+1:04d}',
            'patient_name': f'{first_name} {surname}',
            'age': age,
            'gender': random.choice(['Male', 'Female']),
            'diagnosis': diagnosis,
            'admission_type': random.choice(['Emergency', 'Elective']),
            'length_of_stay': random.randint(1, 14),
            'department': random.choice(['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU']),
            'outcome': random.choice(['Discharged', 'Transferred', 'Improved', 'Stable']),
            'admission_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        })

    df_demographics = pd.DataFrame(demographics_data)
    df_demographics.to_csv('sample_data/patient_demographics_demo.csv', index=False)

    # 4. Staff Performance Data
    print("  👨‍⚕️ Creating staff_performance_demo.csv...")

    staff_data = []
    for date in dates:
        staff_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'physicians_on_duty': random.randint(15, 25),
            'nurses_on_duty': random.randint(40, 60),
            'technicians_on_duty': random.randint(10, 20),
            'support_staff_on_duty': random.randint(20, 35),
            'staff_efficiency_score': round(random.uniform(75, 95), 1),
            'patient_satisfaction_score': round(random.uniform(80, 98), 1),
            'overtime_hours': random.randint(5, 25),
            'staff_shortage_incidents': random.randint(0, 3)
        })

    df_staff = pd.DataFrame(staff_data)
    df_staff.to_csv('sample_data/staff_performance_demo.csv', index=False)

    # 5. Medication Usage Data
    print("  💊 Creating medication_usage_demo.csv...")

    medications = [
        'Paracetamol', 'Amoxicillin', 'Chloroquine', 'Artemether', 'Insulin',
        'Metformin', 'Amlodipine', 'Atenolol', 'Furosemide', 'Prednisolone'
    ]

    medication_data = []
    for date in dates:
        for medication in medications:
            stock_level = random.randint(50, 1000)
            reorder_level = random.randint(100, 200)
            units_dispensed = random.randint(10, 100)

            medication_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'medication_name': medication,
                'stock_level': stock_level,
                'reorder_level': reorder_level,
                'units_dispensed': units_dispensed,
                'stock_status': 'Low' if stock_level < reorder_level else 'Normal',
                'cost_per_unit': round(random.uniform(0.5, 50.0), 2),
                'expiry_alert': random.choice(['None', 'Warning', 'Critical']) if random.random() > 0.8 else 'None'
            })

    df_medications = pd.DataFrame(medication_data)
    df_medications.to_csv('sample_data/medication_usage_demo.csv', index=False)

    print("  ✅ Created 5 comprehensive CSV files for ML demonstration")
    print("    📁 Files saved in 'sample_data/' directory:")
    print("      - hospital_admissions_demo.csv (365 days of admission data)")
    print("      - resource_utilization_demo.csv (daily resource metrics)")
    print("      - patient_demographics_demo.csv (500 patient records)")
    print("      - staff_performance_demo.csv (daily staff metrics)")
    print("      - medication_usage_demo.csv (medication stock data)")

def create_basic_hospital_data():
    """Create basic hospital data for demonstration."""
    print("\n🏥 Creating basic hospital data...")

    # Ensure we have at least one hospital
    hospital, created = Hospital.objects.get_or_create(
        name='HUTANO Demo Hospital',
        defaults={
            'location': 'Harare, Zimbabwe',
            'district': 'Harare',
            'province': 'Harare',
            'bed_capacity': 500,
            'is_rural': False
        }
    )

    if created:
        print(f"  ✅ Created: {hospital.name}")
    else:
        print(f"  ♻️  Using existing: {hospital.name}")

    # Create basic departments
    departments = ['Emergency', 'Internal Medicine', 'Surgery', 'Pediatrics', 'ICU']
    for dept_name in departments:
        dept, created = Department.objects.get_or_create(
            hospital=hospital,
            name=dept_name,
            defaults={'description': f'{dept_name} department'}
        )

    print(f"  ✅ Created {len(departments)} departments")

def main():
    """Main function to run demo data generation."""
    print("🏥 HUTANO Simple Demo Data Generator")
    print("=" * 50)

    # Step 1: Clear existing data safely
    clear_demo_data()

    # Step 2: Create basic hospital structure
    create_basic_hospital_data()

    # Step 3: Create sample CSV files
    create_sample_csv_files()

    print("\n" + "=" * 50)
    print("✅ DEMO DATA GENERATION COMPLETE!")
    print("=" * 50)

    print(f"\n🎯 DEMONSTRATION HIGHLIGHTS:")
    print(f"✅ 5 comprehensive CSV files for ML model testing")
    print(f"✅ Realistic Zimbabwe hospital data patterns")
    print(f"✅ Seasonal and weekly admission variations")
    print(f"✅ Authentic Zimbabwean patient names and diagnoses")
    print(f"✅ 365 days of historical data for forecasting")

    print(f"\n📊 FILES CREATED:")
    print(f"📈 hospital_admissions_demo.csv - Daily admission patterns")
    print(f"🏥 resource_utilization_demo.csv - Resource usage metrics")
    print(f"👥 patient_demographics_demo.csv - Patient information")
    print(f"👨‍⚕️ staff_performance_demo.csv - Staff metrics")
    print(f"💊 medication_usage_demo.csv - Medication inventory")

    print(f"\n🌐 NEXT STEPS:")
    print(f"1. Start Django server: python manage.py runserver")
    print(f"2. Navigate to: http://localhost:8000/data-upload/")
    print(f"3. Upload the CSV files to test ML models")
    print(f"4. View predictions and analytics dashboards")
    print(f"5. Explore all system features with realistic data!")

if __name__ == "__main__":
    main()
