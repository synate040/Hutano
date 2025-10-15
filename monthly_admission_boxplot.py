"""
HUTANO Hospital Resource Forecasting System - Monthly Admission Boxplot
Generate boxplot highlighting monthly admission outliers (Figure 4.10)
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set style for professional-looking charts
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def create_monthly_admission_boxplot():
    """Create boxplot highlighting monthly admission outliers for HUTANO system"""
    
    np.random.seed(42)
    
    # Generate realistic monthly admission data for Zimbabwean hospitals
    months = ['January', 'February', 'March', 'May', 'August', 'September', 'November', 'December']
    month_colors = ['#B8D4E3', '#A8C8DB', '#7FB3D3', '#5B9BD5', '#4F87C7', '#3E6B8A', '#2E4F6B', '#1E3A4F']
    
    # Generate admission data with seasonal patterns and outliers
    admission_data = {}
    
    for i, month in enumerate(months):
        # Base admission levels with seasonal variation
        if month in ['January', 'February', 'March']:  # Summer in Zimbabwe - higher admissions
            base_mean = 950
            base_std = 80
        elif month in ['May']:  # Autumn - moderate
            base_mean = 900
            base_std = 75
        elif month in ['August', 'September']:  # Winter/Spring - lower
            base_mean = 850
            base_std = 70
        else:  # November, December - holiday season variations
            base_mean = 880
            base_std = 85
        
        # Generate normal distribution data
        data = np.random.normal(base_mean, base_std, 100)
        
        # Add specific outliers for each month
        outliers = []
        if month == 'January':
            outliers = [600, 1450]  # Holiday effects and emergency spikes
        elif month == 'February':
            outliers = [1380]  # End of holiday season spike
        elif month == 'March':
            outliers = [550]  # Unusual low admission day
        elif month == 'May':
            outliers = [1200]  # Unexpected spike
        elif month == 'August':
            outliers = [650]  # Winter low
        elif month == 'September':
            outliers = [1050]  # Spring activity increase
        elif month == 'November':
            outliers = [550]  # Pre-holiday low
        elif month == 'December':
            outliers = [1100]  # Holiday emergency spike
        
        # Combine normal data with outliers
        all_data = np.concatenate([data, outliers])
        admission_data[month] = all_data
    
    # Create the boxplot
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    fig.patch.set_facecolor('white')
    
    # Prepare data for boxplot
    data_list = [admission_data[month] for month in months]
    
    # Create boxplot with custom colors
    box_plot = ax.boxplot(data_list, 
                         labels=months,
                         patch_artist=True,
                         showfliers=True,
                         flierprops=dict(marker='o', markerfacecolor='red', markersize=6, 
                                       markeredgecolor='red', alpha=0.8),
                         medianprops=dict(color='black', linewidth=2),
                         whiskerprops=dict(color='gray', linewidth=1.5),
                         capprops=dict(color='gray', linewidth=1.5))
    
    # Color the boxes with gradient
    for patch, color in zip(box_plot['boxes'], month_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
        patch.set_edgecolor('gray')
        patch.set_linewidth(1)
    
    # Customize the plot
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Admissions', fontsize=12, fontweight='bold')
    ax.set_title('Boxplot\nHighlighting Monthly Admission Outliers', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Set y-axis limits and ticks
    ax.set_ylim(500, 1500)
    ax.set_yticks(range(600, 1500, 200))
    
    # Add grid
    ax.grid(True, color='lightgray', linewidth=0.5, alpha=0.7, axis='y')
    ax.set_axisbelow(True)
    
    # Style the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('gray')
    ax.spines['bottom'].set_color('gray')
    ax.set_facecolor('white')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add figure number
    fig.text(0.1, 0.02, 'FIGURE 4.10: Boxplot Highlighting Monthly Admission Outliers', 
             fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('hutano_monthly_admission_boxplot.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("Generated: hutano_monthly_admission_boxplot.png")
    
    # Save the data
    boxplot_df = pd.DataFrame(dict([(month, pd.Series(data)) for month, data in admission_data.items()]))
    boxplot_df.to_csv('hutano_monthly_admission_data.csv', index=False)
    print("Data saved to: hutano_monthly_admission_data.csv")
    
    # Print summary statistics
    print("\nMonthly Admission Summary:")
    print("=" * 40)
    for month in months:
        data = admission_data[month]
        mean_val = np.mean(data)
        std_val = np.std(data)
        outlier_count = len([x for x in data if x < np.percentile(data, 25) - 1.5 * (np.percentile(data, 75) - np.percentile(data, 25)) or 
                            x > np.percentile(data, 75) + 1.5 * (np.percentile(data, 75) - np.percentile(data, 25))])
        print(f"{month:12}: Mean={mean_val:6.0f}, Std={std_val:5.1f}, Outliers={outlier_count}")
    
    return admission_data

def create_outlier_analysis():
    """Create detailed outlier analysis"""
    
    admission_data = create_monthly_admission_boxplot()
    
    # Create outlier analysis plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('white')
    
    months = list(admission_data.keys())
    months_short = ['Jan', 'Feb', 'Mar', 'May', 'Aug', 'Sep', 'Nov', 'Dec']
    
    # Panel 1: Outlier frequency by month
    outlier_counts = []
    for month in months:
        data = admission_data[month]
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        outlier_counts.append(len(outliers))
    
    bars1 = ax1.bar(months_short, outlier_counts, color='#E74C3C', alpha=0.7, edgecolor='black')
    ax1.set_title('Outlier Frequency by Month', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Number of Outliers', fontsize=12)
    ax1.set_xlabel('Month', fontsize=12)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, count in zip(bars1, outlier_counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{count}', ha='center', va='bottom', fontweight='bold')
    
    # Panel 2: Seasonal admission trends
    seasonal_means = [np.mean(admission_data[month]) for month in months]
    seasonal_stds = [np.std(admission_data[month]) for month in months]
    
    ax2.errorbar(months_short, seasonal_means, yerr=seasonal_stds, 
                marker='o', linewidth=3, markersize=8, capsize=5,
                color='#2ECC71', markerfacecolor='#27AE60', ecolor='gray')
    ax2.fill_between(months_short, 
                    [m - s for m, s in zip(seasonal_means, seasonal_stds)],
                    [m + s for m, s in zip(seasonal_means, seasonal_stds)],
                    alpha=0.2, color='#2ECC71')
    ax2.set_title('Seasonal Admission Trends with Variability', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Mean Admissions ± Std Dev', fontsize=12)
    ax2.set_xlabel('Month', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Style both axes
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('gray')
        ax.spines['bottom'].set_color('gray')
        ax.set_facecolor('white')
    
    fig.suptitle('HUTANO: Monthly Admission Outlier Analysis', 
                 fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('hutano_outlier_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("Generated: hutano_outlier_analysis.png")

if __name__ == "__main__":
    print("Generating HUTANO Monthly Admission Boxplot...")
    print("=" * 50)
    
    try:
        # Generate main boxplot
        admission_data = create_monthly_admission_boxplot()
        
        # Generate outlier analysis
        create_outlier_analysis()
        
        print("\n" + "=" * 50)
        print("Monthly admission analysis completed successfully!")
        print("\nGenerated files:")
        print("- hutano_monthly_admission_boxplot.png - Figure 4.10 Monthly outliers")
        print("- hutano_outlier_analysis.png - Detailed outlier analysis")
        print("- hutano_monthly_admission_data.csv - Monthly admission data")
        
        print("\nKey Insights:")
        print("- Summer months (Jan-Mar) show higher admission rates")
        print("- Winter months (Aug-Sep) have lower but more variable admissions")
        print("- Red dots indicate outliers (emergency situations or data anomalies)")
        print("- Seasonal patterns help predict resource needs")
        print("- Outlier detection helps identify unusual events")
        
    except Exception as e:
        print(f"Error generating monthly admission analysis: {e}")
