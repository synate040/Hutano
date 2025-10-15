"""
Script to check available hospitals.
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

# Import models after Django setup
from core.models import Hospital

# Get all hospitals
hospitals = Hospital.objects.all()
print(f"Found {hospitals.count()} hospitals:")

# Print hospital details
for hospital in hospitals:
    print(f"ID: {hospital.id}, Name: {hospital.name}")

# Check data files
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
print(f"\nChecking data files in {data_dir}:")

# List all admissions_*_processed.csv files
import glob
data_files = glob.glob(os.path.join(data_dir, "admissions_*_processed.csv"))
print(f"Found {len(data_files)} data files:")

for file in data_files:
    filename = os.path.basename(file)
    print(f"- {filename}")
