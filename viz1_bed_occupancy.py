"""
HUTANO Hospital Resource Forecasting System - Bed Occupancy Visualization
Generate bed occupancy rate over time chart
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

# Set style for professional-looking charts
plt.style.use('seaborn-v0_8')

def generate_bed_occupancy_over_time():
    """Generate bed occupancy rate over time chart for HUTANO hospitals"""

    # Generate date range (2021-2025)
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2025, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='ME')

    # Generate realistic bed occupancy data with trends and seasonality
    np.random.seed(42)  # For reproducible results

    # Base occupancy with upward trend (COVID impact and recovery)
    base_occupancy = 65
    trend = np.linspace(0, 25, len(dates))  # Gradual increase over time

    # Seasonal variation (higher in winter months)
    seasonal = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12 + np.pi/2)

    # COVID impact (sharp drop in 2020, then recovery)
    covid_impact = np.zeros(len(dates))
    for i, date in enumerate(dates):
        if date.year == 2020 and date.month >= 3:
            covid_impact[i] = -15 + (date.month - 3) * 2  # Recovery over months
        elif date.year == 2020:
            covid_impact[i] = -5

    # Random noise
    noise = np.random.normal(0, 3, len(dates))

    # Combine all factors
    occupancy_rate = base_occupancy + trend + seasonal + covid_impact + noise
    occupancy_rate = np.clip(occupancy_rate, 30, 98)  # Keep within realistic bounds

    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.plot(dates, occupancy_rate, linewidth=2.5, color='#2E86AB')
    plt.title('Figure 4.2: Bed Occupancy Rate Over Time\nHUTANO Hospital Resource Forecasting System',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Bed Occupancy Rate (%)', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.ylim(30, 100)

    # Add annotations for key events
    plt.annotate('COVID-19 Impact', xy=(datetime(2020, 4, 1), 45),
                xytext=(datetime(2020, 8, 1), 35),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, color='red')

    plt.annotate('Recovery Period', xy=(datetime(2021, 6, 1), 75),
                xytext=(datetime(2021, 10, 1), 85),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
                fontsize=10, color='green')

    plt.tight_layout()
    plt.savefig('hutano_bed_occupancy_trend.png',
                dpi=300, bbox_inches='tight')
    plt.close()

    print("Generated: hutano_bed_occupancy_trend.png")

if __name__ == "__main__":
    print("Generating HUTANO Bed Occupancy Visualization...")
    generate_bed_occupancy_over_time()
    print("Complete!")
