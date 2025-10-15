"""
Script to copy processed data files to the prediction data directory.
"""
import os
import shutil

# Source directory (where the processed files are)
source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')

# Ensure the source directory exists
os.makedirs(source_dir, exist_ok=True)

# List of hospital IDs
hospital_ids = range(1, 33)  # 1 through 32

# Copy files for each hospital
for hospital_id in hospital_ids:
    source_file = os.path.join(source_dir, f'admissions_{hospital_id}_processed.csv')
    
    # Check if the source file exists
    if os.path.exists(source_file):
        print(f"File exists: {source_file}")
    else:
        print(f"File does not exist: {source_file}")

print("Done checking files.")
