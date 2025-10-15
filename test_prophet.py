"""
Script to test Prophet forecasting directly.
"""
import os
import sys
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Enable verbose output
print("Starting Prophet test script...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
try:
    import prophet
    print(f"Prophet package: {prophet}")
except Exception as e:
    print(f"Error importing prophet package: {e}")

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

    # Ensure date column is in datetime format
    data['ds'] = pd.to_datetime(data['ds'])

    # Create and train Prophet model
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
    future = model.make_future_dataframe(periods=30)
    print(f"Generating forecast for {len(future)} periods")
    forecast = model.predict(future)
    print("Forecast generated successfully")

    # Save forecast plot
    fig = model.plot(forecast)
    plt.title(f'{data_type.title()} Forecast for Hospital {hospital_id}')
    plt.xlabel('Date')
    plt.ylabel(data_type.replace('_', ' ').title())
    plot_path = os.path.join(output_dir, f"{data_type}_{hospital_id}_forecast.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Forecast plot saved to {plot_path}")

    # Save components plot
    fig = model.plot_components(forecast)
    plot_path = os.path.join(output_dir, f"{data_type}_{hospital_id}_components.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Components plot saved to {plot_path}")

    # Save forecast to CSV
    forecast_path = os.path.join(output_dir, f"{data_type}_{hospital_id}_forecast.csv")
    forecast.to_csv(forecast_path, index=False)
    print(f"Forecast saved to {forecast_path}")

    print("Done!")
else:
    print(f"Data file not found: {data_file}")
    print(f"Directory contents: {os.listdir(data_dir)}")
