"""
Script to implement bed occupancy forecasting.
This script will:
1. Create a model for bed occupancy forecasting
2. Enable the bed occupancy forecast button in the dashboard
3. Process sample bed occupancy data
"""
import os
import django
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

# Import models after Django setup
from prediction.models import PredictionModel, ResourceDemandPrediction
from core.models import Hospital, BedAllocation
from prediction.prophet_forecasting import HutanoProphetForecaster

def create_bed_occupancy_model():
    """Create a model for bed occupancy forecasting."""
    print("Creating bed occupancy model...")
    
    # Get or create the Prophet model for bed occupancy
    model, created = PredictionModel.objects.get_or_create(
        name="Prophet Bed Occupancy Forecast",
        model_type="prophet",
        defaults={
            'description': "Facebook Prophet model for forecasting bed occupancy",
            'parameters': {'seasonality_mode': 'additive', 'horizon': 30}
        }
    )
    
    if created:
        print("Created new bed occupancy model")
    else:
        print("Using existing bed occupancy model")
    
    return model

def generate_sample_bed_data(hospital_id):
    """Generate sample bed occupancy data for a hospital."""
    print(f"Generating sample bed occupancy data for hospital ID {hospital_id}...")
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate sample data
    start_date = datetime.now() - timedelta(days=365)
    dates = pd.date_range(start=start_date, periods=365, freq='D')
    
    # Create a realistic pattern with:
    # - Weekly seasonality (higher on weekends)
    # - Monthly seasonality (higher at month end)
    # - Yearly seasonality (higher in winter months)
    # - Upward trend
    
    # Base occupancy (50-80% of capacity)
    hospital = Hospital.objects.get(id=hospital_id)
    capacity = hospital.bed_capacity or 100  # Default to 100 if not set
    base_occupancy = capacity * 0.65  # 65% average occupancy
    
    # Weekly pattern (higher on weekends)
    day_of_week = dates.dayofweek
    weekly_pattern = np.where(day_of_week >= 5, capacity * 0.1, 0)  # 10% higher on weekends
    
    # Monthly pattern (higher at month end)
    day_of_month = dates.day
    monthly_pattern = np.where(day_of_month >= 25, capacity * 0.05, 0)  # 5% higher at month end
    
    # Yearly pattern (higher in winter)
    month = dates.month
    yearly_pattern = np.where((month <= 2) | (month >= 11), capacity * 0.15, 
                     np.where((month >= 3) & (month <= 5), capacity * 0.05, 0))  # Higher in winter, slightly higher in spring
    
    # Trend (slight increase over time)
    trend = np.linspace(0, capacity * 0.1, 365)  # 10% increase over the year
    
    # Random noise
    noise = np.random.normal(0, capacity * 0.03, 365)  # 3% random variation
    
    # Combine all components
    occupancy = base_occupancy + weekly_pattern + monthly_pattern + yearly_pattern + trend + noise
    
    # Ensure values are within reasonable bounds (not negative, not over capacity)
    occupancy = np.clip(occupancy, capacity * 0.4, capacity * 0.95)
    
    # Round to integers
    occupancy = np.round(occupancy).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'ds': dates,
        'y': occupancy
    })
    
    # Save to CSV
    file_path = os.path.join(data_dir, f"bed_occupancy_{hospital_id}_processed.csv")
    data.to_csv(file_path, index=False)
    print(f"Sample data saved to {file_path}")
    
    return data, file_path

def generate_bed_occupancy_forecast(hospital_id):
    """Generate bed occupancy forecast for a hospital."""
    print(f"Generating bed occupancy forecast for hospital ID {hospital_id}...")
    
    # Get the hospital
    hospital = Hospital.objects.get(id=hospital_id)
    
    # Get the model
    model = create_bed_occupancy_model()
    
    # Generate sample data if needed
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
    data_file = os.path.join(data_dir, f"bed_occupancy_{hospital_id}_processed.csv")
    
    if not os.path.exists(data_file):
        data, _ = generate_sample_bed_data(hospital_id)
    else:
        # Load existing data
        data = pd.read_csv(data_file)
        data['ds'] = pd.to_datetime(data['ds'])
    
    # Create forecaster and train model
    print(f"Creating forecaster for hospital_id={hospital_id}")
    forecaster = HutanoProphetForecaster(hospital_id=hospital_id, data_type='bed_occupancy')
    
    print(f"Training model with {len(data)} records")
    forecaster.train_model(data)
    
    # Generate forecast
    print(f"Generating forecast for 30 periods")
    forecast = forecaster.generate_forecast(periods=30)
    print(f"Forecast generated with {len(forecast)} records")
    
    # Save forecast plots
    print(f"Saving forecast plots")
    forecaster.plot_forecast()
    forecaster.plot_components()
    
    # Save predictions to database
    print(f"Saving predictions to database")
    future_forecast = forecast.tail(30)  # Only future predictions
    
    # Delete existing predictions
    ResourceDemandPrediction.objects.filter(
        hospital=hospital,
        prediction_model=model,
        resource_type='bed'
    ).delete()
    
    for i, (_, row) in enumerate(future_forecast.iterrows()):
        prediction_date = row['ds'].date()
        
        # Create prediction
        prediction = ResourceDemandPrediction.objects.create(
            hospital=hospital,
            prediction_model=model,
            resource_type='bed',
            prediction_date=prediction_date,
            predicted_demand=int(row['yhat']),
            confidence_interval_lower=int(row['yhat_lower']),
            confidence_interval_upper=int(row['yhat_upper'])
        )
        
        if i < 5:  # Print first 5 predictions for debugging
            print(f"Created prediction for {prediction_date}: {int(row['yhat'])}")
    
    print(f"Created {len(future_forecast)} bed occupancy predictions for {hospital.name}")
    return True

if __name__ == "__main__":
    # Process all hospitals
    hospitals = Hospital.objects.all()
    print(f"Found {hospitals.count()} hospitals")
    
    for hospital in hospitals:
        print(f"\nProcessing hospital: {hospital.name} (ID: {hospital.id})")
        generate_bed_occupancy_forecast(hospital.id)
    
    print("\nBed occupancy forecasting implemented successfully!")
    print("Now you need to update the dashboard template to enable the button.")
