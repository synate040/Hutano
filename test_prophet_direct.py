"""
Script to test Prophet forecasting directly.
This script bypasses the Django views and tests the Prophet forecasting directly.
"""
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import numpy as np

# Set up paths
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'data')
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction', 'forecasts')
os.makedirs(output_dir, exist_ok=True)

# Hospital ID to test
hospital_id = 1
data_type = 'admissions'

# Load data
data_file = os.path.join(data_dir, f'{data_type}_{hospital_id}_processed.csv')
print(f"Loading data from {data_file}")
print(f"File exists: {os.path.exists(data_file)}")

if os.path.exists(data_file):
    # Load the data
    data = pd.read_csv(data_file)
    print(f"Loaded {len(data)} records")
    print(f"First 5 rows: {data.head()}")
    print(f"Data types: {data.dtypes}")
    
    # Ensure date column is in datetime format
    data['ds'] = pd.to_datetime(data['ds'])
    print(f"Data range: {data['ds'].min()} to {data['ds'].max()}")
    print(f"Value range: min={data['y'].min()}, max={data['y'].max()}, mean={data['y'].mean()}")
    
    # Create and train Prophet model
    print("Creating Prophet model...")
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='additive',
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10.0
    )
    
    print("Training model...")
    model.fit(data)
    print("Model trained successfully")
    
    # Generate forecast
    periods = 30
    print(f"Generating forecast for {periods} periods")
    future = model.make_future_dataframe(periods=periods)
    print(f"Future dataframe shape: {future.shape}")
    forecast = model.predict(future)
    print(f"Forecast generated with {len(forecast)} records")
    print(f"Forecast range: {forecast['ds'].min()} to {forecast['ds'].max()}")
    
    # Print the last 5 rows of the forecast (future predictions)
    print("Future predictions:")
    print(forecast.tail(5)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
    
    # Save forecast plot
    print("Generating forecast plot...")
    fig = model.plot(forecast)
    plt.title(f'{data_type.title()} Forecast for Hospital {hospital_id}')
    plt.xlabel('Date')
    plt.ylabel(data_type.replace('_', ' ').title())
    plot_path = os.path.join(output_dir, f"{data_type}_{hospital_id}_forecast.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Forecast plot saved to {plot_path}")
    
    # Save components plot
    print("Generating components plot...")
    fig = model.plot_components(forecast)
    plot_path = os.path.join(output_dir, f"{data_type}_{hospital_id}_components.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Components plot saved to {plot_path}")
    
    # Save forecast to CSV
    forecast_path = os.path.join(output_dir, f"{data_type}_{hospital_id}_forecast.csv")
    forecast.to_csv(forecast_path, index=False)
    print(f"Forecast saved to {forecast_path}")
    
    # Generate a new forecast with different data
    print("\nGenerating a new forecast with different data...")
    
    # Create synthetic data with a clear trend
    dates = pd.date_range(start='2024-01-01', periods=365)
    trend = np.linspace(10, 50, 365)  # Increasing trend from 10 to 50
    seasonality = 10 * np.sin(np.linspace(0, 2*np.pi, 365))  # Yearly seasonality
    noise = np.random.normal(0, 2, 365)  # Random noise
    values = trend + seasonality + noise
    
    synthetic_data = pd.DataFrame({
        'ds': dates,
        'y': values
    })
    
    # Save synthetic data
    synthetic_data_path = os.path.join(output_dir, f"synthetic_{data_type}_{hospital_id}.csv")
    synthetic_data.to_csv(synthetic_data_path, index=False)
    print(f"Synthetic data saved to {synthetic_data_path}")
    
    # Train model on synthetic data
    print("Training model on synthetic data...")
    model2 = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='additive',
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10.0
    )
    model2.fit(synthetic_data)
    
    # Generate forecast
    future2 = model2.make_future_dataframe(periods=periods)
    forecast2 = model2.predict(future2)
    
    # Save forecast plot
    fig = model2.plot(forecast2)
    plt.title(f'Synthetic {data_type.title()} Forecast for Hospital {hospital_id}')
    plot_path = os.path.join(output_dir, f"synthetic_{data_type}_{hospital_id}_forecast.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Synthetic forecast plot saved to {plot_path}")
    
    print("Done!")
else:
    print(f"Data file not found: {data_file}")
    print(f"Directory contents: {os.listdir(data_dir)}")
