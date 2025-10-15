"""
HUTANO Hospital Resource Forecasting System - Correlation Heatmap
Generate Pearson correlation heatmap of key hospital variables
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Set style for professional-looking charts
plt.style.use('seaborn-v0_8')

def generate_correlation_heatmap():
    """Generate Pearson correlation heatmap for HUTANO hospital variables"""
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # Generate realistic hospital data for correlation analysis
    n_samples = 200  # Number of observations (days/weeks)
    
    # Generate correlated hospital variables
    
    # Monthly Admissions (base variable)
    monthly_admissions = np.random.normal(850, 120, n_samples)
    monthly_admissions = np.clip(monthly_admissions, 600, 1200)
    
    # Bed Occupancy (slightly negatively correlated with admissions - capacity constraints)
    bed_occupancy = 85 - 0.02 * monthly_admissions + np.random.normal(0, 8, n_samples)
    bed_occupancy = np.clip(bed_occupancy, 60, 98)
    
    # ICU Admissions (negatively correlated with monthly admissions - different patient types)
    icu_admissions = 25 - 0.01 * monthly_admissions + np.random.normal(0, 3, n_samples)
    icu_admissions = np.clip(icu_admissions, 8, 35)
    
    # Length of Stay (positively correlated with bed occupancy, slightly with admissions)
    length_of_stay = 3.5 + 0.02 * bed_occupancy + 0.001 * monthly_admissions + np.random.normal(0, 0.8, n_samples)
    length_of_stay = np.clip(length_of_stay, 2.0, 8.0)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Monthly Admissions': monthly_admissions,
        'Bed Occupancy': bed_occupancy,
        'ICU Admissions': icu_admissions,
        'Length of Stay': length_of_stay
    })
    
    # Calculate correlation matrix
    correlation_matrix = data.corr()
    
    # Create the heatmap
    plt.figure(figsize=(10, 8))
    
    # Create heatmap with custom styling
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))  # Mask upper triangle
    
    # Custom colormap (blue to red)
    cmap = sns.diverging_palette(250, 10, as_cmap=True)
    
    # Create heatmap
    sns.heatmap(correlation_matrix, 
                annot=True,           # Show correlation values
                cmap=cmap,            # Color scheme
                center=0,             # Center colormap at 0
                square=True,          # Square cells
                fmt='.2f',            # Format to 2 decimal places
                cbar_kws={'shrink': 0.8, 'label': 'Correlation Coefficient'},
                linewidths=0.5,       # Add lines between cells
                linecolor='white')
    
    # Customize the plot
    plt.title('Pearson Correlation Heatmap of Key Variables\nHUTANO Hospital Resource Forecasting System', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Add figure number
    plt.figtext(0.02, 0.02, 'FIGURE 4.5: Pearson Correlation Heatmap of Key Variables', 
                fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('hutano_correlation_heatmap.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generated: hutano_correlation_heatmap.png")
    
    # Print correlation insights
    print("\nCorrelation Analysis Results:")
    print("=" * 40)
    for i, var1 in enumerate(correlation_matrix.columns):
        for j, var2 in enumerate(correlation_matrix.columns):
            if i < j:  # Only print upper triangle
                corr_val = correlation_matrix.iloc[i, j]
                print(f"{var1} vs {var2}: {corr_val:.3f}")
    
    # Save correlation data
    correlation_matrix.to_csv('hutano_correlation_data.csv')
    print("\nCorrelation matrix saved to: hutano_correlation_data.csv")
    
    return correlation_matrix

def generate_extended_correlation_analysis():
    """Generate extended correlation analysis with more variables"""
    
    np.random.seed(42)
    n_samples = 150
    
    # Generate more hospital variables
    monthly_admissions = np.random.normal(850, 120, n_samples)
    monthly_admissions = np.clip(monthly_admissions, 600, 1200)
    
    bed_occupancy = 85 - 0.02 * monthly_admissions + np.random.normal(0, 8, n_samples)
    bed_occupancy = np.clip(bed_occupancy, 60, 98)
    
    icu_admissions = 25 - 0.01 * monthly_admissions + np.random.normal(0, 3, n_samples)
    icu_admissions = np.clip(icu_admissions, 8, 35)
    
    length_of_stay = 3.5 + 0.02 * bed_occupancy + 0.001 * monthly_admissions + np.random.normal(0, 0.8, n_samples)
    length_of_stay = np.clip(length_of_stay, 2.0, 8.0)
    
    # Additional variables
    staff_utilization = 70 + 0.015 * monthly_admissions + 0.1 * bed_occupancy + np.random.normal(0, 5, n_samples)
    staff_utilization = np.clip(staff_utilization, 50, 95)
    
    medication_usage = 100 + 0.08 * monthly_admissions + 2 * icu_admissions + np.random.normal(0, 15, n_samples)
    medication_usage = np.clip(medication_usage, 80, 300)
    
    # Create extended DataFrame
    extended_data = pd.DataFrame({
        'Monthly Admissions': monthly_admissions,
        'Bed Occupancy': bed_occupancy,
        'ICU Admissions': icu_admissions,
        'Length of Stay': length_of_stay,
        'Staff Utilization': staff_utilization,
        'Medication Usage': medication_usage
    })
    
    # Calculate extended correlation matrix
    extended_corr = extended_data.corr()
    
    # Create extended heatmap
    plt.figure(figsize=(12, 10))
    
    # Create heatmap
    sns.heatmap(extended_corr, 
                annot=True,
                cmap='RdBu_r',
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={'shrink': 0.8, 'label': 'Correlation Coefficient'},
                linewidths=0.5,
                linecolor='white')
    
    plt.title('Extended Correlation Analysis - HUTANO Hospital Variables\nComprehensive Resource Relationship Matrix', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig('hutano_extended_correlation_heatmap.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generated: hutano_extended_correlation_heatmap.png")
    
    return extended_corr

if __name__ == "__main__":
    print("Generating HUTANO Correlation Heatmap Analysis...")
    print("=" * 60)
    
    try:
        # Generate main correlation heatmap
        corr_matrix = generate_correlation_heatmap()
        
        # Generate extended analysis
        extended_corr = generate_extended_correlation_analysis()
        
        print("=" * 60)
        print("Correlation analysis completed successfully!")
        print("\nGenerated files:")
        print("- hutano_correlation_heatmap.png - Main correlation heatmap (4 variables)")
        print("- hutano_extended_correlation_heatmap.png - Extended analysis (6 variables)")
        print("- hutano_correlation_data.csv - Correlation matrix data")
        
        print("\nKey Insights:")
        print("- Correlation values range from -1 (perfect negative) to +1 (perfect positive)")
        print("- Values near 0 indicate weak or no linear relationship")
        print("- Red colors indicate negative correlations")
        print("- Blue colors indicate positive correlations")
        
    except Exception as e:
        print(f"Error generating correlation analysis: {e}")
