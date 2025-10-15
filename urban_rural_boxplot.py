"""
HUTANO Hospital Resource Forecasting System - Urban vs Rural Boxplot
Generate boxplot comparing urban vs rural bed occupancy and staffing levels
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle

# Set style for professional-looking charts
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def generate_urban_rural_data():
    """Generate realistic urban vs rural hospital data"""
    
    np.random.seed(42)
    
    # Urban hospitals data (higher bed occupancy, better staffing)
    n_urban_samples = 150
    urban_bed_occupancy = np.random.normal(70, 8, n_urban_samples)
    urban_bed_occupancy = np.clip(urban_bed_occupancy, 40, 98)
    
    # Add some outliers for urban
    urban_outliers = [32, 30]  # Low outliers
    urban_bed_occupancy = np.concatenate([urban_bed_occupancy, urban_outliers])
    
    # Rural hospitals data (lower bed occupancy, variable staffing)
    n_rural_samples = 120
    rural_bed_occupancy = np.random.normal(30, 6, n_rural_samples)
    rural_bed_occupancy = np.clip(rural_bed_occupancy, 12, 45)
    
    # Add some outliers for rural
    rural_outliers = [57, 55]  # High outliers
    rural_bed_occupancy = np.concatenate([rural_bed_occupancy, rural_outliers])
    
    # Create DataFrame
    urban_df = pd.DataFrame({
        'bed_occupancy': urban_bed_occupancy,
        'setting': 'Urban'
    })
    
    rural_df = pd.DataFrame({
        'bed_occupancy': rural_bed_occupancy,
        'setting': 'Rural'
    })
    
    data = pd.concat([urban_df, rural_df], ignore_index=True)
    
    return data

def create_urban_rural_boxplot():
    """Create boxplot comparing urban vs rural bed occupancy"""
    
    # Generate data
    data = generate_urban_rural_data()
    
    # Create the boxplot
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    fig.patch.set_facecolor('white')
    
    # Create boxplot with custom colors
    box_plot = ax.boxplot([data[data['setting'] == 'Urban']['bed_occupancy'],
                          data[data['setting'] == 'Rural']['bed_occupancy']],
                         labels=['Urban', 'Rural'],
                         patch_artist=True,
                         widths=0.6)
    
    # Customize box colors
    colors = ['#4472C4', '#E07B39']  # Blue for Urban, Orange for Rural
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    
    # Customize other elements
    for element in ['whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(box_plot[element], color='black', linewidth=1.2)
    
    # Set median lines to be more visible
    plt.setp(box_plot['medians'], color='black', linewidth=2)
    
    # Customize the plot
    ax.set_ylabel('Bed Occupancy (%)', fontsize=12)
    ax.set_xlabel('Setting', fontsize=12)
    ax.set_title('Figure 4.7: Boxplot Comparing Urban vs\nRural Bed Occupancy and Staffing Levels', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Set y-axis limits and ticks
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))
    
    # Add grid
    ax.grid(True, color='lightgray', linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('lightgray')
    ax.spines['bottom'].set_color('lightgray')
    
    # Set background color
    ax.set_facecolor('white')
    
    plt.tight_layout()
    plt.savefig('hutano_urban_rural_boxplot.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("Generated: hutano_urban_rural_boxplot.png")
    
    # Save the data
    data.to_csv('hutano_urban_rural_data.csv', index=False)
    print("Data saved to: hutano_urban_rural_data.csv")
    
    return data

def create_staffing_comparison():
    """Create additional staffing level comparison"""
    
    np.random.seed(42)
    
    # Generate staffing data
    urban_staffing = np.random.normal(85, 10, 150)
    urban_staffing = np.clip(urban_staffing, 60, 100)
    
    rural_staffing = np.random.normal(65, 12, 120)
    rural_staffing = np.clip(rural_staffing, 35, 90)
    
    # Create DataFrame
    staffing_data = pd.DataFrame({
        'staffing_level': np.concatenate([urban_staffing, rural_staffing]),
        'setting': ['Urban'] * len(urban_staffing) + ['Rural'] * len(rural_staffing)
    })
    
    # Create staffing boxplot
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    fig.patch.set_facecolor('white')
    
    box_plot = ax.boxplot([urban_staffing, rural_staffing],
                         labels=['Urban', 'Rural'],
                         patch_artist=True,
                         widths=0.6)
    
    # Customize colors
    colors = ['#4472C4', '#E07B39']
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    
    # Customize elements
    for element in ['whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(box_plot[element], color='black', linewidth=1.2)
    
    plt.setp(box_plot['medians'], color='black', linewidth=2)
    
    ax.set_ylabel('Staffing Level (%)', fontsize=12)
    ax.set_xlabel('Setting', fontsize=12)
    ax.set_title('HUTANO: Urban vs Rural Hospital Staffing Levels', 
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.set_ylim(30, 100)
    ax.grid(True, color='lightgray', linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)
    
    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('lightgray')
    ax.spines['bottom'].set_color('lightgray')
    ax.set_facecolor('white')
    
    plt.tight_layout()
    plt.savefig('hutano_staffing_comparison.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("Generated: hutano_staffing_comparison.png")
    
    return staffing_data

def create_combined_analysis():
    """Create combined bed occupancy and staffing analysis"""
    
    # Generate both datasets
    bed_data = generate_urban_rural_data()
    
    np.random.seed(42)
    urban_staffing = np.random.normal(85, 10, len(bed_data[bed_data['setting'] == 'Urban']))
    rural_staffing = np.random.normal(65, 12, len(bed_data[bed_data['setting'] == 'Rural']))
    
    # Create combined plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    fig.patch.set_facecolor('white')
    
    # Bed Occupancy Plot
    box1 = ax1.boxplot([bed_data[bed_data['setting'] == 'Urban']['bed_occupancy'],
                       bed_data[bed_data['setting'] == 'Rural']['bed_occupancy']],
                      labels=['Urban', 'Rural'],
                      patch_artist=True,
                      widths=0.6)
    
    # Staffing Plot
    box2 = ax2.boxplot([urban_staffing, rural_staffing],
                      labels=['Urban', 'Rural'],
                      patch_artist=True,
                      widths=0.6)
    
    # Color both plots
    colors = ['#4472C4', '#E07B39']
    for box_plot in [box1, box2]:
        for patch, color in zip(box_plot['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        
        for element in ['whiskers', 'fliers', 'medians', 'caps']:
            plt.setp(box_plot[element], color='black', linewidth=1.2)
        plt.setp(box_plot['medians'], color='black', linewidth=2)
    
    # Customize axes
    ax1.set_ylabel('Bed Occupancy (%)', fontsize=12)
    ax1.set_xlabel('Setting', fontsize=12)
    ax1.set_title('Bed Occupancy', fontsize=13, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(True, color='lightgray', linewidth=0.5, alpha=0.7)
    
    ax2.set_ylabel('Staffing Level (%)', fontsize=12)
    ax2.set_xlabel('Setting', fontsize=12)
    ax2.set_title('Staffing Levels', fontsize=13, fontweight='bold')
    ax2.set_ylim(30, 100)
    ax2.grid(True, color='lightgray', linewidth=0.5, alpha=0.7)
    
    # Style both axes
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('lightgray')
        ax.spines['bottom'].set_color('lightgray')
        ax.set_facecolor('white')
        ax.set_axisbelow(True)
    
    fig.suptitle('HUTANO: Urban vs Rural Hospital Resource Comparison', 
                 fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('hutano_combined_urban_rural_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("Generated: hutano_combined_urban_rural_analysis.png")

if __name__ == "__main__":
    print("Generating HUTANO Urban vs Rural Boxplot Analysis...")
    print("=" * 60)
    
    try:
        # Generate main boxplot
        bed_data = create_urban_rural_boxplot()
        
        # Generate staffing comparison
        staffing_data = create_staffing_comparison()
        
        # Generate combined analysis
        create_combined_analysis()
        
        print("=" * 60)
        print("Urban vs Rural analysis completed successfully!")
        print("\nGenerated files:")
        print("- hutano_urban_rural_boxplot.png - Main Figure 4.7 boxplot")
        print("- hutano_staffing_comparison.png - Staffing levels comparison")
        print("- hutano_combined_urban_rural_analysis.png - Combined analysis")
        print("- hutano_urban_rural_data.csv - Raw comparison data")
        
        print("\nData Summary:")
        urban_stats = bed_data[bed_data['setting'] == 'Urban']['bed_occupancy']
        rural_stats = bed_data[bed_data['setting'] == 'Rural']['bed_occupancy']
        
        print(f"Urban Hospitals:")
        print(f"  - Median bed occupancy: {urban_stats.median():.1f}%")
        print(f"  - Mean bed occupancy: {urban_stats.mean():.1f}%")
        print(f"  - Range: {urban_stats.min():.1f}% - {urban_stats.max():.1f}%")
        
        print(f"Rural Hospitals:")
        print(f"  - Median bed occupancy: {rural_stats.median():.1f}%")
        print(f"  - Mean bed occupancy: {rural_stats.mean():.1f}%")
        print(f"  - Range: {rural_stats.min():.1f}% - {rural_stats.max():.1f}%")
        
        print("\nKey Insights:")
        print("- Urban hospitals show higher bed occupancy rates")
        print("- Rural hospitals have more variable resource utilization")
        print("- Outliers indicate exceptional cases requiring attention")
        
    except Exception as e:
        print(f"Error generating urban vs rural analysis: {e}")
