"""
Script to implement staff forecasting.
This script will:
1. Create a model for staff requirement forecasting
2. Generate sample staff requirement data
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
from core.models import Hospital
from prediction.prophet_forecasting import HutanoProphetForecaster

def create_staff_model():
    """Create a model for staff requirement forecasting."""
    print("Creating staff requirement model...")
    
    # Get or create the Prophet model for staff requirements
    model, created = PredictionModel.objects.get_or_create(
        name="Prophet Staff Requirement Forecast",
        model_type="prophet",
        defaults={
            'description': "Facebook Prophet model for forecasting staff requirements",
            'parameters': {'seasonality_mode': 'additive', 'horizon': 30}
        }
    )
    
    if created:
        print("Created new staff requirement model")
    else:
        print("Using existing staff requirement model")
    
    return model

def generate_sample_staff_data(hospital_id):
    """Generate sample staff requirement data for a hospital."""
    print(f"Generating sample staff requirement data for hospital ID {hospital_id}...")
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate sample data
    start_date = datetime.now() - timedelta(days=365)
    dates = pd.date_range(start=start_date, periods=365, freq='D')
    
    # Create a realistic pattern with:
    # - Weekly seasonality (higher on weekdays)
    # - Monthly seasonality (higher at month end)
    # - Yearly seasonality (higher in winter months)
    # - Upward trend
    
    # Base staff requirement (50-100 staff per day)
    hospital = Hospital.objects.get(id=hospital_id)
    base_staff = 75  # Base staff requirement
    
    # Weekly pattern (higher on weekdays, lower on weekends)
    day_of_week = dates.dayofweek
    weekly_pattern = np.where(day_of_week < 5, 15, -10)  # Higher on weekdays, lower on weekends
    
    # Monthly pattern (higher at month end)
    day_of_month = dates.day
    monthly_pattern = np.where(day_of_month >= 25, 10, 0)  # Higher at month end
    
    # Yearly pattern (higher in winter)
    month = dates.month
    yearly_pattern = np.where((month <= 2) | (month >= 11), 20, 
                     np.where((month >= 3) & (month <= 5), 10, 0))  # Higher in winter, slightly higher in spring
    
    # Trend (slight increase over time)
    trend = np.linspace(0, 15, 365)  # 15 staff increase over the year
    
    # Random noise
    noise = np.random.normal(0, 5, 365)  # Random variation
    
    # Combine all components
    staff = base_staff + weekly_pattern + monthly_pattern + yearly_pattern + trend + noise
    
    # Ensure values are within reasonable bounds (not negative)
    staff = np.clip(staff, 40, 150)
    
    # Round to integers
    staff = np.round(staff).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'ds': dates,
        'y': staff
    })
    
    # Save to CSV
    file_path = os.path.join(data_dir, f"staff_{hospital_id}_processed.csv")
    data.to_csv(file_path, index=False)
    print(f"Sample data saved to {file_path}")
    
    return data, file_path

def generate_staff_forecast(hospital_id=2):
    """Generate staff requirement forecast for a hospital."""
    print(f"Generating staff requirement forecast for hospital ID {hospital_id}...")
    
    # Get the hospital
    hospital = Hospital.objects.get(id=hospital_id)
    
    # Get the model
    model = create_staff_model()
    
    # Generate sample data if needed
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
    data_file = os.path.join(data_dir, f"staff_{hospital_id}_processed.csv")
    
    if not os.path.exists(data_file):
        data, _ = generate_sample_staff_data(hospital_id)
    else:
        # Load existing data
        data = pd.read_csv(data_file)
        data['ds'] = pd.to_datetime(data['ds'])
    
    # Create a simple model without hyperparameter tuning
    print(f"Creating a simple model without hyperparameter tuning")
    
    # Create a Prophet model with default parameters
    from prophet import Prophet
    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='additive',
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10.0
    )
    
    # Fit the model
    print(f"Fitting model with {len(data)} records")
    prophet_model.fit(data)
    
    # Generate forecast
    print(f"Generating forecast for 30 periods")
    future = prophet_model.make_future_dataframe(periods=30)
    forecast = prophet_model.predict(future)
    print(f"Forecast generated with {len(forecast)} records")
    
    # Save forecast plots
    print(f"Saving forecast plots")
    import matplotlib.pyplot as plt
    
    # Create forecasts directory if it doesn't exist
    forecasts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'forecasts')
    os.makedirs(forecasts_dir, exist_ok=True)
    
    # Save forecast plot
    fig = prophet_model.plot(forecast)
    plt.title(f'Staff Requirement Forecast for {hospital.name}')
    plt.savefig(os.path.join(forecasts_dir, f"staff_{hospital_id}_forecast.png"), dpi=300, bbox_inches='tight')
    
    # Save components plot
    fig = prophet_model.plot_components(forecast)
    plt.savefig(os.path.join(forecasts_dir, f"staff_{hospital_id}_components.png"), dpi=300, bbox_inches='tight')
    
    # Save predictions to database
    print(f"Saving predictions to database")
    future_forecast = forecast.tail(30)  # Only future predictions
    
    # Delete existing predictions
    ResourceDemandPrediction.objects.filter(
        hospital=hospital,
        prediction_model=model,
        resource_type='staff'
    ).delete()
    
    for i, (_, row) in enumerate(future_forecast.iterrows()):
        prediction_date = row['ds'].date()
        
        # Create prediction
        prediction = ResourceDemandPrediction.objects.create(
            hospital=hospital,
            prediction_model=model,
            resource_type='staff',
            prediction_date=prediction_date,
            predicted_demand=int(row['yhat']),
            confidence_interval_lower=int(row['yhat_lower']),
            confidence_interval_upper=int(row['yhat_upper'])
        )
        
        if i < 5:  # Print first 5 predictions for debugging
            print(f"Created prediction for {prediction_date}: {int(row['yhat'])}")
    
    print(f"Created {len(future_forecast)} staff requirement predictions for {hospital.name}")
    return True

if __name__ == "__main__":
    # Process one hospital (Parirenyatwa Group of Hospitals)
    generate_staff_forecast(hospital_id=2)
    
    print("\nStaff requirement forecasting implemented successfully!")
