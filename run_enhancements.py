"""
Script to run all enhancements for the HUTANO system.
This script will:
1. Implement staff forecasting
2. Run anomaly detection on existing data
3. Set up automated data collection
"""
import os
import django
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

# Import models after Django setup
from core.models import Hospital
from prediction.models import PredictionModel, ResourceDemandPrediction
from prediction.anomaly_detection import AnomalyDetector, detect_anomalies
from prediction.data_collector import HospitalDataCollector, collect_data_for_all_hospitals

def implement_staff_forecasting():
    """Implement staff forecasting for all hospitals."""
    logger.info("Implementing staff forecasting...")
    
    # Create staff forecasting model
    model, created = PredictionModel.objects.get_or_create(
        name="Prophet Staff Requirement Forecast",
        model_type="prophet",
        defaults={
            'description': "Facebook Prophet model for forecasting staff requirements",
            'parameters': {'seasonality_mode': 'additive', 'horizon': 30}
        }
    )
    
    if created:
        logger.info("Created new staff requirement model")
    else:
        logger.info("Using existing staff requirement model")
    
    # Get all hospitals
    hospitals = Hospital.objects.all()
    logger.info(f"Found {hospitals.count()} hospitals")
    
    for hospital in hospitals:
        logger.info(f"Processing hospital: {hospital.name} (ID: {hospital.id})")
        
        # Generate sample staff data
        collector = HospitalDataCollector(hospital.id)
        data = collector.collect_staff_data()
        
        # Create a simple Prophet model
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
        logger.info(f"Fitting model with {len(data)} records")
        prophet_model.fit(data)
        
        # Generate forecast
        logger.info(f"Generating forecast for 30 periods")
        future = prophet_model.make_future_dataframe(periods=30)
        forecast = prophet_model.predict(future)
        logger.info(f"Forecast generated with {len(forecast)} records")
        
        # Save forecast plots
        logger.info(f"Saving forecast plots")
        import matplotlib.pyplot as plt
        
        # Create forecasts directory if it doesn't exist
        forecasts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'forecasts')
        os.makedirs(forecasts_dir, exist_ok=True)
        
        # Save forecast plot
        fig = prophet_model.plot(forecast)
        plt.title(f'Staff Requirement Forecast for {hospital.name}')
        plt.savefig(os.path.join(forecasts_dir, f"staff_{hospital.id}_forecast.png"), dpi=300, bbox_inches='tight')
        
        # Save components plot
        fig = prophet_model.plot_components(forecast)
        plt.savefig(os.path.join(forecasts_dir, f"staff_{hospital.id}_components.png"), dpi=300, bbox_inches='tight')
        
        # Save predictions to database
        logger.info(f"Saving predictions to database")
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
                logger.info(f"Created prediction for {prediction_date}: {int(row['yhat'])}")
        
        logger.info(f"Created {len(future_forecast)} staff requirement predictions for {hospital.name}")

def run_anomaly_detection():
    """Run anomaly detection on existing data."""
    logger.info("Running anomaly detection...")
    
    # Get data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'anomalies')
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all processed data files
    import glob
    data_files = glob.glob(os.path.join(data_dir, "*_processed.csv"))
    logger.info(f"Found {len(data_files)} data files")
    
    for data_file in data_files:
        file_name = os.path.basename(data_file)
        logger.info(f"Detecting anomalies in {file_name}...")
        
        try:
            # Load data
            data = pd.read_csv(data_file)
            data['ds'] = pd.to_datetime(data['ds'])
            
            # Initialize anomaly detector
            detector = AnomalyDetector(contamination=0.05)
            detector.fit(data)
            
            # Detect anomalies
            result = detector.predict(data)
            
            # Save results
            output_file = os.path.join(output_dir, file_name.replace('_processed.csv', '_anomalies.csv'))
            result.to_csv(output_file, index=False)
            
            # Plot anomalies
            output_plot = os.path.join(output_dir, file_name.replace('_processed.csv', '_anomalies.png'))
            detector.plot_anomalies(result, output_plot)
            
            # Log results
            anomaly_count = result['anomaly'].sum()
            logger.info(f"Found {anomaly_count} anomalies in {len(result)} records")
        except Exception as e:
            logger.error(f"Error detecting anomalies in {file_name}: {str(e)}")

def setup_automated_data_collection():
    """Set up automated data collection."""
    logger.info("Setting up automated data collection...")
    
    # Collect data for all hospitals
    collect_data_for_all_hospitals()
    
    # Schedule data collection
    from prediction.data_collector import schedule_data_collection
    schedule_data_collection(interval_hours=24)
    
    logger.info("Automated data collection set up successfully")

def main():
    """Main function to run all enhancements."""
    logger.info("Running all enhancements for HUTANO system...")
    
    # Implement staff forecasting
    implement_staff_forecasting()
    
    # Run anomaly detection
    run_anomaly_detection()
    
    # Set up automated data collection
    setup_automated_data_collection()
    
    logger.info("All enhancements completed successfully!")

if __name__ == "__main__":
    main()
