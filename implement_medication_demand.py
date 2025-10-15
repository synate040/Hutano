"""
Script to implement medication demand forecasting.
This script will:
1. Create a model for medication demand forecasting
2. Generate sample medication demand data
3. Process the data and generate forecasts
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
from core.models import Hospital, MedicationInventory
from prediction.prophet_forecasting import HutanoProphetForecaster

def create_medication_model():
    """Create a model for medication demand forecasting."""
    print("Creating medication demand model...")
    
    # Get or create the Prophet model for medication demand
    model, created = PredictionModel.objects.get_or_create(
        name="Prophet Medication Demand Forecast",
        model_type="prophet",
        defaults={
            'description': "Facebook Prophet model for forecasting medication demand",
            'parameters': {'seasonality_mode': 'additive', 'horizon': 30}
        }
    )
    
    if created:
        print("Created new medication demand model")
    else:
        print("Using existing medication demand model")
    
    return model

def generate_sample_medication_data(hospital_id):
    """Generate sample medication demand data for a hospital."""
    print(f"Generating sample medication demand data for hospital ID {hospital_id}...")
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate sample data
    start_date = datetime.now() - timedelta(days=365)
    dates = pd.date_range(start=start_date, periods=365, freq='D')
    
    # Create a realistic pattern with:
    # - Weekly seasonality (higher on weekdays)
    # - Monthly seasonality (higher at month beginning)
    # - Yearly seasonality (higher in flu season)
    # - Upward trend
    
    # Base demand (100-200 units per day)
    base_demand = 150
    
    # Weekly pattern (higher on weekdays, lower on weekends)
    day_of_week = dates.dayofweek
    weekly_pattern = np.where(day_of_week < 5, 30, -20)  # Higher on weekdays, lower on weekends
    
    # Monthly pattern (higher at month beginning)
    day_of_month = dates.day
    monthly_pattern = np.where(day_of_month <= 5, 40, 0)  # Higher at month beginning
    
    # Yearly pattern (higher in flu season)
    month = dates.month
    yearly_pattern = np.where((month >= 5) & (month <= 8), -30,  # Lower in summer
                     np.where((month >= 11) | (month <= 2), 50, 0))  # Higher in winter
    
    # Trend (slight increase over time)
    trend = np.linspace(0, 50, 365)  # 50 unit increase over the year
    
    # Random noise
    noise = np.random.normal(0, 15, 365)  # Random variation
    
    # Combine all components
    demand = base_demand + weekly_pattern + monthly_pattern + yearly_pattern + trend + noise
    
    # Ensure values are within reasonable bounds (not negative)
    demand = np.clip(demand, 50, 400)
    
    # Round to integers
    demand = np.round(demand).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'ds': dates,
        'y': demand
    })
    
    # Save to CSV
    file_path = os.path.join(data_dir, f"medication_{hospital_id}_processed.csv")
    data.to_csv(file_path, index=False)
    print(f"Sample data saved to {file_path}")
    
    return data, file_path

def generate_medication_forecast(hospital_id):
    """Generate medication demand forecast for a hospital."""
    print(f"Generating medication demand forecast for hospital ID {hospital_id}...")
    
    # Get the hospital
    hospital = Hospital.objects.get(id=hospital_id)
    
    # Get the model
    model = create_medication_model()
    
    # Generate sample data if needed
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
    data_file = os.path.join(data_dir, f"medication_{hospital_id}_processed.csv")
    
    if not os.path.exists(data_file):
        data, _ = generate_sample_medication_data(hospital_id)
    else:
        # Load existing data
        data = pd.read_csv(data_file)
        data['ds'] = pd.to_datetime(data['ds'])
    
    # Create forecaster and train model
    print(f"Creating forecaster for hospital_id={hospital_id}")
    forecaster = HutanoProphetForecaster(hospital_id=hospital_id, data_type='medication')
    
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
        resource_type='medication'
    ).delete()
    
    for i, (_, row) in enumerate(future_forecast.iterrows()):
        prediction_date = row['ds'].date()
        
        # Create prediction
        prediction = ResourceDemandPrediction.objects.create(
            hospital=hospital,
            prediction_model=model,
            resource_type='medication',
            prediction_date=prediction_date,
            predicted_demand=int(row['yhat']),
            confidence_interval_lower=int(row['yhat_lower']),
            confidence_interval_upper=int(row['yhat_upper'])
        )
        
        if i < 5:  # Print first 5 predictions for debugging
            print(f"Created prediction for {prediction_date}: {int(row['yhat'])}")
    
    print(f"Created {len(future_forecast)} medication demand predictions for {hospital.name}")
    return True

if __name__ == "__main__":
    # Process all hospitals
    hospitals = Hospital.objects.all()
    print(f"Found {hospitals.count()} hospitals")
    
    for hospital in hospitals:
        print(f"\nProcessing hospital: {hospital.name} (ID: {hospital.id})")
        generate_medication_forecast(hospital.id)
    
    print("\nMedication demand forecasting implemented successfully!")
