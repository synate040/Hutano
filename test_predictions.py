#!/usr/bin/env python
"""
Test script to demonstrate the prediction comparison system
"""
import os
import sys
import django
from datetime import datetime, timedelta
import pandas as pd

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, DocumentUpload, PredictionComparison
from core.services.data_processor import DataProcessor

def test_prediction_system():
    """Test the prediction comparison system"""
    print("🧪 Testing HUTANO Prediction System...")
    
    # Get a hospital
    hospital = Hospital.objects.first()
    if not hospital:
        print("❌ No hospital found. Please create a hospital first.")
        return
    
    print(f"🏥 Using hospital: {hospital.name}")
    
    # Create a mock document upload
    document_upload = DocumentUpload.objects.create(
        hospital=hospital,
        document_type='patient_data',
        original_filename='test_patient_data.csv',
        file_size=1024,
        processing_status='processing'
    )
    
    print(f"📄 Created document upload: {document_upload.id}")
    
    # Create sample patient data
    sample_data = pd.DataFrame({
        'patient_id': [f'PAT-{i:03d}' for i in range(1, 16)],
        'age': [25, 34, 45, 67, 23, 56, 78, 29, 41, 52, 33, 48, 61, 37, 44],
        'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M'],
        'admission_date': [
            (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') 
            for i in range(15, 0, -1)
        ],
        'diagnosis': [
            'Malaria', 'Hypertension', 'Diabetes', 'Pneumonia', 'Tuberculosis',
            'HIV/AIDS', 'Stroke', 'Heart Disease', 'Cancer', 'Asthma',
            'Malnutrition', 'Mental Health', 'Road Traffic Injury', 'Maternal', 'Diarrhea'
        ],
        'department': [
            'Internal Medicine', 'Cardiology', 'Endocrinology', 'Respiratory', 'Infectious Disease',
            'Internal Medicine', 'Neurology', 'Cardiology', 'Oncology', 'Respiratory',
            'Nutrition', 'Psychiatry', 'Emergency', 'Obstetrics', 'Gastroenterology'
        ],
        'is_emergency': [False, True, False, True, False, True, True, False, False, True, False, False, True, True, False]
    })
    
    print(f"📊 Created sample data with {len(sample_data)} patient records")
    
    # Initialize data processor
    processor = DataProcessor(hospital, document_upload)
    
    # Process the data
    print("🔄 Processing data and generating predictions...")
    result = processor.process_document(sample_data.to_csv(index=False).encode())
    
    if result['success']:
        print("✅ Data processing successful!")
        print(f"   📈 Created: {result['result']['created']} records")
        print(f"   🔄 Updated: {result['result']['updated']} records")
        print(f"   🧠 Insights: {len(result.get('insights', []))} generated")
        
        if 'predictions' in result:
            predictions = result['predictions']
            if 'improvement_metrics' in predictions:
                metrics = predictions['improvement_metrics']
                print(f"   🎯 Prediction Improvement: {metrics['improvement']:.1f}%")
                print(f"   📊 Before Accuracy: {metrics['before_accuracy']:.1f}%")
                print(f"   📈 After Accuracy: {metrics['after_accuracy']:.1f}%")
                
                # Get the prediction comparison
                comparison_id = predictions.get('comparison_id')
                if comparison_id:
                    comparison = PredictionComparison.objects.get(id=comparison_id)
                    print(f"   🔗 Prediction Comparison ID: {comparison_id}")
                    print(f"   📅 Created: {comparison.created_at}")
                    print(f"   🏥 Hospital: {comparison.hospital.name}")
                    
                    # Show URL for viewing
                    print(f"\n🌐 View detailed comparison at:")
                    print(f"   http://127.0.0.1:8000/core/predictions/{comparison_id}/")
            else:
                print("   ⚠️ No prediction metrics available")
        else:
            print("   ⚠️ No predictions generated")
    else:
        print(f"❌ Data processing failed: {result.get('error', 'Unknown error')}")
    
    print("\n🎉 Test completed!")
    print("\n📋 Summary:")
    print(f"   • Hospital: {hospital.name}")
    print(f"   • Document Upload ID: {document_upload.id}")
    print(f"   • Total Predictions: {PredictionComparison.objects.count()}")
    print(f"   • Dashboard URL: http://127.0.0.1:8000/core/data-upload/")

if __name__ == "__main__":
    test_prediction_system()
