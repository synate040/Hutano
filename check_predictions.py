"""
Script to check and fix prediction values in the database.
"""
import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

# Import models after Django setup
from prediction.models import PatientAdmissionPrediction, PredictionModel
from core.models import Hospital

def check_predictions():
    """Check the current prediction values in the database."""
    print("Checking prediction values in the database...")
    
    # Get all hospitals
    hospitals = Hospital.objects.all()
    print(f"Found {hospitals.count()} hospitals")
    
    # Get all prediction models
    models = PredictionModel.objects.all()
    print(f"Found {models.count()} prediction models")
    
    # Get all predictions
    predictions = PatientAdmissionPrediction.objects.all().order_by('-prediction_date')
    print(f"Found {predictions.count()} predictions")
    
    # Print the first 10 predictions
    print("\nRecent predictions:")
    for i, p in enumerate(predictions[:10]):
        print(f"{i+1}. Date: {p.prediction_date}, Hospital: {p.hospital.name}, " +
              f"Model: {p.prediction_model.model_type}, Value: {p.predicted_admissions}")
    
    # Check for duplicate predictions for the same date
    dates = {}
    duplicates = 0
    for p in predictions:
        key = (p.prediction_date, p.hospital.id)
        if key in dates:
            dates[key] += 1
            duplicates += 1
        else:
            dates[key] = 1
    
    print(f"\nFound {duplicates} duplicate predictions for the same date and hospital")
    
    # Print dates with multiple predictions
    if duplicates > 0:
        print("\nDates with multiple predictions:")
        for (date, hospital_id), count in dates.items():
            if count > 1:
                hospital = Hospital.objects.get(id=hospital_id)
                print(f"Date: {date}, Hospital: {hospital.name}, Count: {count}")
    
    return predictions, models, hospitals

def fix_predictions():
    """Fix prediction values by updating them from the processed data files."""
    print("\nFixing prediction values...")
    
    # Get all predictions, models, and hospitals
    predictions, models, hospitals = check_predictions()
    
    # Get the Prophet model
    try:
        prophet_model = PredictionModel.objects.get(model_type='prophet')
        print(f"Found Prophet model: {prophet_model.name}")
    except PredictionModel.DoesNotExist:
        print("Prophet model not found. Creating one...")
        prophet_model = PredictionModel.objects.create(
            name="Prophet Admission Forecast",
            model_type="prophet",
            description="Facebook Prophet model for forecasting hospital resources",
            parameters={'seasonality_mode': 'additive', 'horizon': 30}
        )
    
    # Process each hospital
    for hospital in hospitals:
        print(f"\nProcessing hospital: {hospital.name} (ID: {hospital.id})")
        
        # Check if there's a processed data file for this hospital
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
        data_file = os.path.join(data_dir, f"admissions_{hospital.id}_processed.csv")
        
        if os.path.exists(data_file):
            print(f"Found data file: {data_file}")
            
            # Load the data
            data = pd.read_csv(data_file)
            print(f"Loaded {len(data)} records")
            
            # Check the data values
            print(f"Data range: min={data['y'].min()}, max={data['y'].max()}, mean={data['y'].mean():.2f}")
            
            # Get existing predictions for this hospital
            hospital_predictions = PatientAdmissionPrediction.objects.filter(
                hospital=hospital,
                prediction_model=prophet_model
            )
            print(f"Found {hospital_predictions.count()} existing predictions for this hospital")
            
            # Delete existing predictions if they don't match the data
            if hospital_predictions.exists():
                first_pred = hospital_predictions.first()
                if first_pred.predicted_admissions > 30:  # Assuming your data is in the range 5-27
                    print(f"Existing predictions seem too high (e.g., {first_pred.predicted_admissions})")
                    print("Deleting existing predictions...")
                    hospital_predictions.delete()
                    print(f"Deleted {hospital_predictions.count()} predictions")
        else:
            print(f"No data file found for hospital {hospital.id}")
    
    print("\nPrediction check and fix completed.")

if __name__ == "__main__":
    fix_predictions()
