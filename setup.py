#!/usr/bin/env python3
"""
HUTANO Setup Script
Automates the installation and setup of the HUTANO Hospital Resource Forecasting System
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   {e.stderr}")
        return False

def setup_hutano():
    """Main setup function"""
    print("🏥 HUTANO Hospital Resource Forecasting System Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your internet connection.")
        sys.exit(1)
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
    django.setup()
    
    # Run migrations
    print("\n🔄 Setting up database...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Database setup completed!")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        sys.exit(1)
    
    # Create sample hospitals
    print("\n🔄 Creating sample hospitals...")
    try:
        from core.models import Hospital
        
        hospitals = [
            'Parirenyatwa Group of Hospitals',
            'Sally Mugabe Central Hospital', 
            'Mpilo Central Hospital',
            'Chitungwiza Central Hospital',
            'United Bulawayo Hospitals',
            'Gweru Provincial Hospital',
            'Bindura Provincial Hospital',
            'Karanda Mission Hospital'
        ]
        
        created_count = 0
        for name in hospitals:
            hospital, created = Hospital.objects.get_or_create(
                name=name, 
                defaults={'location': 'Zimbabwe', 'description': f'{name} - Major healthcare facility'}
            )
            if created:
                created_count += 1
        
        print(f"✅ Created {created_count} hospitals!")
        
    except Exception as e:
        print(f"❌ Failed to create hospitals: {e}")
    
    # Create sample prediction data
    print("\n🔄 Creating sample prediction data...")
    try:
        from core.models import PredictionComparison, DocumentUpload
        from django.contrib.auth.models import User
        import random
        
        # Get or create a user
        user, _ = User.objects.get_or_create(
            username='demo_user',
            defaults={'email': 'demo@hutano.zw', 'is_staff': True}
        )
        
        hospital = Hospital.objects.first()
        if hospital:
            # Create sample prediction comparisons
            for i in range(3):
                doc = DocumentUpload.objects.create(
                    hospital=hospital,
                    document_type='patient_data',
                    original_filename=f'sample_data_{i+1}.csv',
                    file_size=random.randint(500, 2000),
                    processing_status='completed',
                    uploaded_by=user
                )
                
                before_acc = random.uniform(70, 85)
                after_acc = min(95, before_acc + random.uniform(3, 12))
                improvement = ((after_acc - before_acc) / before_acc) * 100
                
                PredictionComparison.objects.create(
                    hospital=hospital,
                    document_upload=doc,
                    prediction_type='admissions',
                    before_prediction_data={'accuracy': before_acc, 'trend': 'increasing'},
                    after_prediction_data={'accuracy': after_acc, 'trend': 'stable'},
                    before_accuracy_score=before_acc,
                    after_accuracy_score=after_acc,
                    improvement_percentage=round(improvement, 1),
                    confidence_change=round(after_acc - before_acc, 1)
                )
            
            print("✅ Sample prediction data created!")
        
    except Exception as e:
        print(f"❌ Failed to create prediction data: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 HUTANO Setup Complete!")
    print("\n📊 Access your system at:")
    print("   Main Dashboard: http://127.0.0.1:8000/core/data-upload/")
    print("   Admin Panel: http://127.0.0.1:8000/admin/")
    print("\n🚀 To start the server, run:")
    print("   python manage.py runserver")
    print("\n📚 Check README.md for more information!")

if __name__ == "__main__":
    setup_hutano()
