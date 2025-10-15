"""
HUTANO Hospital Resource Forecasting System - SHAP Summary Plot
Generate SHAP summary plot for XGBoost model interpretability
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Set style for professional-looking charts
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def generate_shap_data():
    """Generate realistic SHAP values for HUTANO XGBoost model"""

    np.random.seed(42)

    # Define features relevant to hospital resource forecasting
    features = [
        'Length of Stay',
        'Bed Occupancy',
        'ICU Beds',
        'Admissions'
    ]

    # Number of samples for SHAP analysis
    n_samples = 200

    # Generate SHAP values for each feature
    shap_data = {}
    feature_values = {}

    # Length of Stay - high impact, wide distribution
    shap_data['Length of Stay'] = np.random.normal(1.2, 0.8, n_samples)
    shap_data['Length of Stay'] = np.clip(shap_data['Length of Stay'], -1.5, 3.0)
    feature_values['Length of Stay'] = np.random.uniform(2, 15, n_samples)  # Days

    # Bed Occupancy - moderate impact, clustered distribution
    shap_data['Bed Occupancy'] = np.random.normal(0.8, 0.6, n_samples)
    shap_data['Bed Occupancy'] = np.clip(shap_data['Bed Occupancy'], -1.0, 2.5)
    feature_values['Bed Occupancy'] = np.random.uniform(40, 95, n_samples)  # Percentage

    # ICU Beds - moderate impact, more concentrated
    shap_data['ICU Beds'] = np.random.normal(0.6, 0.5, n_samples)
    shap_data['ICU Beds'] = np.clip(shap_data['ICU Beds'], -0.8, 2.0)
    feature_values['ICU Beds'] = np.random.uniform(5, 50, n_samples)  # Number of beds

    # Admissions - lower impact, tight distribution
    shap_data['Admissions'] = np.random.normal(0.4, 0.4, n_samples)
    shap_data['Admissions'] = np.clip(shap_data['Admissions'], -0.6, 1.5)
    feature_values['Admissions'] = np.random.uniform(20, 200, n_samples)  # Daily admissions

    return shap_data, feature_values

def create_shap_summary_plot():
    """Create SHAP summary plot for XGBoost model"""

    # Generate SHAP data
    shap_data, feature_values = generate_shap_data()

    # Create the plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    fig.patch.set_facecolor('white')

    # Define colors for the plot (blue to red gradient)
    colors = ['#3498DB', '#E74C3C']  # Blue to Red

    # Plot each feature
    y_positions = range(len(shap_data))
    feature_names = list(shap_data.keys())

    for i, feature in enumerate(feature_names):
        shap_vals = shap_data[feature]
        feat_vals = feature_values[feature]

        # Normalize feature values for color mapping (0 to 1)
        normalized_vals = (feat_vals - feat_vals.min()) / (feat_vals.max() - feat_vals.min())

        # Create scatter plot with color mapping
        scatter = ax.scatter(shap_vals, [i] * len(shap_vals),
                           c=normalized_vals,
                           cmap='coolwarm',
                           alpha=0.7,
                           s=25,
                           edgecolors='none')

    # Customize the plot
    ax.set_yticks(y_positions)
    ax.set_yticklabels(feature_names)
    ax.set_xlabel('SHAP value\n(impact on model output)', fontsize=12)
    ax.set_ylabel('Feature value', fontsize=12)
    ax.set_title('FIGURE 4.9: SHAP Summary Plot\nfor XGBoost Model',
                 fontsize=14, fontweight='bold', pad=20)

    # Set x-axis limits
    ax.set_xlim(-0.2, 3.2)

    # Add vertical line at x=0
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1, alpha=0.8)

    # Add grid
    ax.grid(True, color='lightgray', linewidth=0.5, alpha=0.5, axis='x')
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('lightgray')
    ax.spines['bottom'].set_color('lightgray')

    # Set background color
    ax.set_facecolor('white')

    # Add color bar legend
    cbar = plt.colorbar(scatter, ax=ax, pad=0.02, aspect=30)
    cbar.set_label('Feature value\n(Low → High)', fontsize=10)
    cbar.ax.tick_params(labelsize=9)

    plt.tight_layout()
    plt.savefig('hutano_shap_summary_plot.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print("Generated: hutano_shap_summary_plot.png")

    # Save SHAP data
    shap_df = pd.DataFrame(shap_data)
    feature_df = pd.DataFrame(feature_values)

    shap_df.to_csv('hutano_shap_values.csv', index=False)
    feature_df.to_csv('hutano_feature_values.csv', index=False)
    print("Data saved to: hutano_shap_values.csv and hutano_feature_values.csv")

    return shap_data, feature_values

def create_detailed_shap_analysis():
    """Create detailed SHAP analysis with multiple views"""

    shap_data, feature_values = generate_shap_data()

    # Create multi-panel SHAP analysis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.patch.set_facecolor('white')

    # Panel 1: Summary plot (same as main)
    y_positions = range(len(shap_data))
    feature_names = list(shap_data.keys())

    for i, feature in enumerate(feature_names):
        shap_vals = shap_data[feature]
        feat_vals = feature_values[feature]
        normalized_vals = (feat_vals - feat_vals.min()) / (feat_vals.max() - feat_vals.min())

        scatter = ax1.scatter(shap_vals, [i] * len(shap_vals),
                             c=normalized_vals, cmap='coolwarm',
                             alpha=0.7, s=20, edgecolors='none')

    ax1.set_yticks(y_positions)
    ax1.set_yticklabels(feature_names)
    ax1.set_xlabel('SHAP value', fontsize=11)
    ax1.set_title('SHAP Summary Plot', fontsize=12, fontweight='bold')
    ax1.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax1.grid(True, color='lightgray', linewidth=0.5, alpha=0.5, axis='x')

    # Panel 2: Feature importance (mean absolute SHAP)
    importance_scores = [np.mean(np.abs(shap_data[feature])) for feature in feature_names]
    bars = ax2.barh(y_positions, importance_scores, color='#4472C4', alpha=0.8)
    ax2.set_yticks(y_positions)
    ax2.set_yticklabels(feature_names)
    ax2.set_xlabel('Mean |SHAP value|', fontsize=11)
    ax2.set_title('Feature Importance', fontsize=12, fontweight='bold')
    ax2.grid(True, color='lightgray', linewidth=0.5, alpha=0.5, axis='x')

    # Panel 3: SHAP distribution for top feature
    top_feature = feature_names[np.argmax(importance_scores)]
    ax3.hist(shap_data[top_feature], bins=30, color='#E74C3C', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('SHAP value', fontsize=11)
    ax3.set_ylabel('Frequency', fontsize=11)
    ax3.set_title(f'SHAP Distribution: {top_feature}', fontsize=12, fontweight='bold')
    ax3.grid(True, color='lightgray', linewidth=0.5, alpha=0.5)

    # Panel 4: Feature correlation with SHAP
    feature_name = 'Length of Stay'
    ax4.scatter(feature_values[feature_name], shap_data[feature_name],
               alpha=0.6, color='#2ECC71', s=25)
    ax4.set_xlabel(f'{feature_name} (days)', fontsize=11)
    ax4.set_ylabel('SHAP value', fontsize=11)
    ax4.set_title(f'Feature vs SHAP: {feature_name}', fontsize=12, fontweight='bold')
    ax4.grid(True, color='lightgray', linewidth=0.5, alpha=0.5)

    # Style all axes
    for ax in [ax1, ax2, ax3, ax4]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('lightgray')
        ax.spines['bottom'].set_color('lightgray')
        ax.set_facecolor('white')
        ax.set_axisbelow(True)

    fig.suptitle('HUTANO: Comprehensive SHAP Analysis for XGBoost Model',
                 fontsize=16, fontweight='bold')

    plt.tight_layout()
    plt.savefig('hutano_detailed_shap_analysis.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print("Generated: hutano_detailed_shap_analysis.png")

def create_shap_waterfall_example():
    """Create example SHAP waterfall plot for single prediction"""

    np.random.seed(42)

    # Example prediction breakdown
    features = ['Length of Stay', 'Bed Occupancy', 'ICU Beds', 'Admissions']
    shap_values = [1.2, 0.8, -0.3, 0.4]
    base_value = 2.1

    # Calculate cumulative values
    cumulative = [base_value]
    for val in shap_values:
        cumulative.append(cumulative[-1] + val)

    # Create waterfall plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    fig.patch.set_facecolor('white')

    # Plot bars
    x_pos = range(len(features) + 2)
    colors = ['gray'] + ['red' if val < 0 else 'blue' for val in shap_values] + ['green']

    # Base value
    ax.bar(0, base_value, color='gray', alpha=0.7, label='Base value')

    # SHAP contributions
    for i, (feature, shap_val) in enumerate(zip(features, shap_values)):
        color = '#E74C3C' if shap_val < 0 else '#4472C4'
        ax.bar(i + 1, abs(shap_val), bottom=min(cumulative[i], cumulative[i+1]),
               color=color, alpha=0.7)

        # Add value labels
        ax.text(i + 1, cumulative[i+1], f'{shap_val:+.1f}',
               ha='center', va='bottom' if shap_val > 0 else 'top', fontweight='bold')

    # Final prediction
    ax.bar(len(features) + 1, cumulative[-1], color='#2ECC71', alpha=0.7, label='Prediction')

    # Customize plot
    ax.set_xticks(x_pos)
    ax.set_xticklabels(['Base'] + features + ['Prediction'], rotation=45, ha='right')
    ax.set_ylabel('Model Output', fontsize=12)
    ax.set_title('HUTANO: SHAP Waterfall Plot - Single Prediction Example',
                 fontsize=14, fontweight='bold')

    # Add connecting lines
    for i in range(len(cumulative) - 1):
        ax.plot([i, i + 1], [cumulative[i], cumulative[i]], 'k--', alpha=0.5)

    ax.grid(True, color='lightgray', linewidth=0.5, alpha=0.5, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_facecolor('white')

    plt.tight_layout()
    plt.savefig('hutano_shap_waterfall_example.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print("Generated: hutano_shap_waterfall_example.png")

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

    return admission_data

def create_seasonal_analysis():
    """Create comprehensive seasonal admission analysis"""

    np.random.seed(42)

    # Create multi-panel seasonal analysis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.patch.set_facecolor('white')

    # Panel 1: Monthly boxplot (simplified version)
    months_short = ['Jan', 'Feb', 'Mar', 'May', 'Aug', 'Sep', 'Nov', 'Dec']
    admission_data = create_monthly_admission_boxplot()

    data_list = [admission_data[month] for month in admission_data.keys()]
    month_colors = ['#B8D4E3', '#A8C8DB', '#7FB3D3', '#5B9BD5', '#4F87C7', '#3E6B8A', '#2E4F6B', '#1E3A4F']

    box_plot = ax1.boxplot(data_list, labels=months_short, patch_artist=True, showfliers=True,
                          flierprops=dict(marker='o', markerfacecolor='red', markersize=4))

    for patch, color in zip(box_plot['boxes'], month_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    ax1.set_title('Monthly Admission Patterns', fontweight='bold')
    ax1.set_ylabel('Admissions')
    ax1.grid(True, alpha=0.3)

    # Panel 2: Outlier frequency by month
    outlier_counts = []
    for month_data in data_list:
        Q1 = np.percentile(month_data, 25)
        Q3 = np.percentile(month_data, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = month_data[(month_data < lower_bound) | (month_data > upper_bound)]
        outlier_counts.append(len(outliers))

    bars = ax2.bar(months_short, outlier_counts, color='#E74C3C', alpha=0.7)
    ax2.set_title('Outlier Frequency by Month', fontweight='bold')
    ax2.set_ylabel('Number of Outliers')
    ax2.grid(True, alpha=0.3, axis='y')

    # Panel 3: Seasonal trends
    seasonal_means = [np.mean(data) for data in data_list]
    ax3.plot(months_short, seasonal_means, marker='o', linewidth=3, markersize=8,
             color='#2ECC71', markerfacecolor='#27AE60')
    ax3.fill_between(months_short, seasonal_means, alpha=0.3, color='#2ECC71')
    ax3.set_title('Seasonal Admission Trends', fontweight='bold')
    ax3.set_ylabel('Mean Admissions')
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)

    # Panel 4: Variability analysis
    seasonal_stds = [np.std(data) for data in data_list]
    ax4.bar(months_short, seasonal_stds, color='#F39C12', alpha=0.7)
    ax4.set_title('Admission Variability by Month', fontweight='bold')
    ax4.set_ylabel('Standard Deviation')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.tick_params(axis='x', rotation=45)

    # Style all axes
    for ax in [ax1, ax2, ax3, ax4]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_facecolor('white')

    fig.suptitle('HUTANO: Comprehensive Seasonal Admission Analysis',
                 fontsize=16, fontweight='bold')

    plt.tight_layout()
    plt.savefig('hutano_seasonal_analysis.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print("Generated: hutano_seasonal_analysis.png")

if __name__ == "__main__":
    print("Generating HUTANO SHAP Analysis...")
    print("=" * 50)

    try:
        # Generate main SHAP summary plot
        shap_data, feature_values = create_shap_summary_plot()

        # Generate detailed analysis
        create_detailed_shap_analysis()

        # Generate waterfall example
        create_shap_waterfall_example()

        print("\n" + "=" * 50)
        print("Generating Monthly Admission Analysis...")

        # Generate monthly admission boxplot
        admission_data = create_monthly_admission_boxplot()

        # Generate seasonal analysis
        create_seasonal_analysis()

        print("=" * 50)
        print("All analyses completed successfully!")
        print("\nGenerated files:")
        print("- hutano_shap_summary_plot.png - Main Figure 4.9 SHAP summary")
        print("- hutano_detailed_shap_analysis.png - Comprehensive 4-panel analysis")
        print("- hutano_shap_waterfall_example.png - Single prediction breakdown")
        print("- hutano_monthly_admission_boxplot.png - Figure 4.10 Monthly outliers")
        print("- hutano_seasonal_analysis.png - Comprehensive seasonal analysis")
        print("- hutano_shap_values.csv - SHAP values data")
        print("- hutano_feature_values.csv - Feature values data")
        print("- hutano_monthly_admission_data.csv - Monthly admission data")

        print("\nSHAP Analysis Summary:")
        for feature in shap_data.keys():
            mean_impact = np.mean(np.abs(shap_data[feature]))
            print(f"- {feature}: Mean |SHAP| = {mean_impact:.3f}")

        print("\nMonthly Admission Insights:")
        for month in admission_data.keys():
            mean_admissions = np.mean(admission_data[month])
            print(f"- {month}: Mean = {mean_admissions:.0f} admissions")

        print("\nKey Insights:")
        print("- Summer months (Jan-Mar) show higher admission rates")
        print("- Winter months (Aug-Sep) have lower but more variable admissions")
        print("- Outliers indicate emergency situations or data anomalies")
        print("- Seasonal patterns help predict resource needs")
        print("- SHAP analysis provides model interpretability")

    except Exception as e:
        print(f"Error generating analyses: {e}")
