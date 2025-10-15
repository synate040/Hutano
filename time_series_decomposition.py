"""
HUTANO Hospital Resource Forecasting System - Time Series Decomposition
Generate time series decomposition for admissions and ICU demand (2019-2022)
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# Set style for professional-looking charts
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def generate_time_series_data():
    """Generate realistic hospital time series data for decomposition"""

    # Set random seed for reproducible results
    np.random.seed(42)

    # Generate daily data from 2019 to 2022
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2022, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')

    n_days = len(dates)

    # Generate admissions data with trend, seasonality, and noise

    # 1. Trend component (gradual increase over time)
    trend = 800 + np.linspace(0, 600, n_days)  # Base 800, increasing to 1400

    # 2. Seasonal component (yearly cycle + weekly cycle)
    # Yearly seasonality (higher in winter months)
    yearly_cycle = 100 * np.sin(2 * np.pi * np.arange(n_days) / 365.25 + np.pi)

    # Weekly seasonality (lower on weekends)
    weekly_cycle = 50 * np.sin(2 * np.pi * np.arange(n_days) / 7)

    seasonal = yearly_cycle + weekly_cycle

    # 3. COVID-19 impact (irregular component)
    covid_impact = np.zeros(n_days)
    for i, date in enumerate(dates):
        if date.year == 2020 and 3 <= date.month <= 8:
            # Sharp drop in March 2020, gradual recovery
            covid_impact[i] = -200 * np.exp(-(date.month - 3) * 0.5)
        elif date.year == 2020 and date.month > 8:
            covid_impact[i] = -50
        elif date.year == 2021:
            covid_impact[i] = -30 + (date.month - 1) * 2  # Gradual recovery

    # 4. Random noise
    noise = np.random.normal(0, 30, n_days)

    # Combine all components
    admissions = trend + seasonal + covid_impact + noise
    admissions = np.clip(admissions, 500, 1800)  # Keep within realistic bounds

    # Generate ICU demand (correlated but different pattern)
    icu_base = 30
    icu_trend = np.linspace(0, 20, n_days)
    icu_seasonal = 5 * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
    icu_covid = covid_impact * 0.1  # Less impact on ICU
    icu_noise = np.random.normal(0, 3, n_days)

    icu_demand = icu_base + icu_trend + icu_seasonal + icu_covid + icu_noise
    icu_demand = np.clip(icu_demand, 15, 70)

    # Create DataFrame
    data = pd.DataFrame({
        'date': dates,
        'admissions': admissions,
        'icu_demand': icu_demand
    })
    data.set_index('date', inplace=True)

    return data

def create_time_series_decomposition():
    """Create time series decomposition visualization matching the reference format"""

    # Generate data
    data = generate_time_series_data()

    # Perform seasonal decomposition for admissions
    decomposition = seasonal_decompose(data['admissions'], model='additive', period=365)

    # Create the decomposition plot with exact formatting
    fig, axes = plt.subplots(4, 1, figsize=(12, 10))
    fig.patch.set_facecolor('white')

    # 1. Original Admissions Data
    axes[0].plot(data.index, data['admissions'], color='#4472C4', linewidth=1.2)
    axes[0].set_title('Admissions', fontsize=11, fontweight='normal', loc='left')
    axes[0].set_ylim(750, 1750)
    axes[0].grid(True, color='lightgray', linewidth=0.5)
    axes[0].set_facecolor('white')

    # 2. Trend Component
    axes[1].plot(data.index, decomposition.trend, color='#4472C4', linewidth=1.5)
    axes[1].set_title('Trend', fontsize=11, fontweight='normal', loc='left')
    axes[1].set_ylabel('Trend', fontsize=10)
    axes[1].grid(True, color='lightgray', linewidth=0.5)
    axes[1].set_facecolor('white')

    # 3. Seasonal Component
    axes[2].plot(data.index, decomposition.seasonal, color='#4472C4', linewidth=1.2)
    axes[2].set_title('Seasonal', fontsize=11, fontweight='normal', loc='left')
    axes[2].set_ylabel('Seasonal', fontsize=10)
    axes[2].grid(True, color='lightgray', linewidth=0.5)
    axes[2].set_facecolor('white')
    axes[2].set_ylim(-150, 150)

    # 4. Residual Component (scatter plot)
    # Sample every 7th point to reduce density like in the reference
    sample_indices = range(0, len(data), 7)
    sample_dates = data.index[sample_indices]
    sample_resid = decomposition.resid.iloc[sample_indices]

    axes[3].scatter(sample_dates, sample_resid, color='#4472C4', alpha=0.7, s=12)
    axes[3].axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    axes[3].set_title('Resid', fontsize=11, fontweight='normal', loc='left')
    axes[3].set_ylabel('Resid', fontsize=10)
    axes[3].grid(True, color='lightgray', linewidth=0.5)
    axes[3].set_facecolor('white')
    axes[3].set_ylim(-60, 80)

    # Set x-axis formatting for all subplots
    for i, ax in enumerate(axes):
        ax.set_xlim(data.index[0], data.index[-1])

        # Only show x-axis labels on bottom plot
        if i < 3:
            ax.set_xticklabels([])
        else:
            # Format x-axis to show years
            years = pd.date_range('2019', '2026', freq='YS')
            ax.set_xticks(years)
            ax.set_xticklabels([str(year.year) for year in years])

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('lightgray')
        ax.spines['bottom'].set_color('lightgray')

    # Main title
    fig.suptitle('Time Series Decomposition –\nAdmissions and ICU Demand (2019–2022)',
                 fontsize=14, fontweight='bold', y=0.95)

    # Add figure caption
    fig.text(0.02, 0.02, 'FIGURE 4.6: Time Series Decomposition - Admissions and ICU Demand (2019–2022)',
             fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.08, hspace=0.3)
    plt.savefig('hutano_time_series_decomposition.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print("Generated: hutano_time_series_decomposition.png")

    # Save the data for reference
    data.to_csv('hutano_time_series_data.csv')
    print("Data saved to: hutano_time_series_data.csv")

    return data, decomposition

def create_icu_demand_analysis():
    """Create additional ICU demand analysis"""

    # Generate data
    data = generate_time_series_data()

    # Create ICU-specific analysis
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    # ICU Demand over time
    axes[0].plot(data.index, data['icu_demand'], color='#E63946', linewidth=1.5, label='ICU Demand')
    axes[0].set_title('ICU Demand Over Time (2019-2022)', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('ICU Patients', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Admissions vs ICU Demand comparison
    # Normalize both series for comparison
    norm_admissions = (data['admissions'] - data['admissions'].min()) / (data['admissions'].max() - data['admissions'].min())
    norm_icu = (data['icu_demand'] - data['icu_demand'].min()) / (data['icu_demand'].max() - data['icu_demand'].min())

    axes[1].plot(data.index, norm_admissions, color='#2E86AB', linewidth=1.5, label='Admissions (Normalized)', alpha=0.8)
    axes[1].plot(data.index, norm_icu, color='#E63946', linewidth=1.5, label='ICU Demand (Normalized)', alpha=0.8)
    axes[1].set_title('Normalized Comparison: Admissions vs ICU Demand', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Normalized Values', fontsize=12)
    axes[1].set_xlabel('Year', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # Format x-axis
    for ax in axes:
        years = pd.date_range('2019', '2025', freq='YS')
        ax.set_xticks(years)
        ax.set_xticklabels([str(year.year) for year in years])

    plt.suptitle('HUTANO Hospital ICU Demand Analysis (2019-2022)',
                 fontsize=16, fontweight='bold')

    plt.tight_layout()
    plt.savefig('hutano_icu_demand_analysis.png',
                dpi=300, bbox_inches='tight')
    plt.close()

    print("Generated: hutano_icu_demand_analysis.png")

if __name__ == "__main__":
    print("Generating HUTANO Time Series Decomposition Analysis...")
    print("=" * 60)

    try:
        # Generate main decomposition
        data, decomposition = create_time_series_decomposition()

        # Generate ICU analysis
        create_icu_demand_analysis()

        print("=" * 60)
        print("Time series analysis completed successfully!")
        print("\nGenerated files:")
        print("- hutano_time_series_decomposition.png - Main decomposition analysis")
        print("- hutano_icu_demand_analysis.png - ICU demand specific analysis")
        print("- hutano_time_series_data.csv - Raw time series data")

        print("\nDecomposition Components:")
        print("- Trend: Long-term movement in the data")
        print("- Seasonal: Regular patterns that repeat over time")
        print("- Residual: Random variations and irregular events")

        print(f"\nData Summary:")
        print(f"- Time period: 2019-2022 ({len(data)} days)")
        print(f"- Average admissions: {data['admissions'].mean():.1f}")
        print(f"- Average ICU demand: {data['icu_demand'].mean():.1f}")

    except Exception as e:
        print(f"Error generating time series analysis: {e}")
