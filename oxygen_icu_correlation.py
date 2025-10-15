"""
HUTANO Hospital Resource Forecasting System - Oxygen Supply vs ICU Admissions Correlation
Generate scatter plot showing correlation between oxygen supply and ICU admissions
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns

# Set style for professional-looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def generate_oxygen_icu_correlation():
    """Generate oxygen supply vs ICU admissions scatter plot for HUTANO hospitals"""
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # Generate realistic data for oxygen supply and ICU admissions
    n_points = 120  # Number of data points (representing different time periods/hospitals)
    
    # Generate oxygen supply data (cylinders per day)
    # Range from 1 to 10 cylinders per day
    oxygen_supply = np.random.uniform(1, 10, n_points)
    
    # Generate ICU admissions with strong positive correlation to oxygen supply
    # Base relationship: more oxygen supply correlates with higher ICU capacity/admissions
    base_icu = 2.0 * oxygen_supply + 1.5  # Linear relationship
    
    # Add some realistic noise and variation
    noise = np.random.normal(0, 1.2, n_points)
    seasonal_effect = 0.8 * np.sin(np.linspace(0, 4*np.pi, n_points))  # Seasonal variation
    
    # Combine factors
    icu_admissions = base_icu + noise + seasonal_effect
    icu_admissions = np.clip(icu_admissions, 0.5, 22)  # Keep within realistic bounds
    
    # Calculate correlation coefficient
    correlation_coef, p_value = stats.pearsonr(oxygen_supply, icu_admissions)
    
    # Create the scatter plot
    plt.figure(figsize=(10, 8))
    
    # Create scatter plot
    plt.scatter(oxygen_supply, icu_admissions, 
               alpha=0.7, s=50, color='#2E86AB', edgecolors='black', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(oxygen_supply, icu_admissions, 1)
    p = np.poly1d(z)
    plt.plot(oxygen_supply, p(oxygen_supply), "r-", linewidth=2.5, alpha=0.8)
    
    # Add correlation coefficient text
    plt.text(0.05, 0.95, f'r = {correlation_coef:.2f}', 
             transform=plt.gca().transAxes, fontsize=14, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Customize the plot
    plt.title('Oxygen Supply vs ICU Admissions (Scatter)\nHUTANO Hospital Resource Forecasting System', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Oxygen Supply (cylinders/day)', fontsize=12, fontweight='bold')
    plt.ylabel('ICU Admissions', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Set axis limits
    plt.xlim(0, 11)
    plt.ylim(0, 22)
    
    # Add some styling
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('hutano_oxygen_icu_correlation.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generated: hutano_oxygen_icu_correlation.png")
    print(f"Correlation coefficient: {correlation_coef:.3f}")
    print(f"P-value: {p_value:.3f}")
    
    # Also create a DataFrame for reference
    data = pd.DataFrame({
        'Oxygen_Supply_Cylinders_Per_Day': oxygen_supply,
        'ICU_Admissions': icu_admissions
    })
    
    # Save the data for future reference
    data.to_csv('hutano_oxygen_icu_data.csv', index=False)
    print("Data saved to: hutano_oxygen_icu_data.csv")
    
    return correlation_coef, p_value

def generate_enhanced_correlation_analysis():
    """Generate additional correlation analysis with multiple variables"""
    
    np.random.seed(42)
    n_points = 100
    
    # Generate multiple correlated variables
    oxygen_supply = np.random.uniform(1, 10, n_points)
    ventilator_usage = 0.7 * oxygen_supply + np.random.normal(0, 0.8, n_points)
    ventilator_usage = np.clip(ventilator_usage, 0, 8)
    
    icu_admissions = 1.8 * oxygen_supply + 0.5 * ventilator_usage + np.random.normal(0, 1.0, n_points)
    icu_admissions = np.clip(icu_admissions, 1, 20)
    
    # Create correlation matrix
    data = pd.DataFrame({
        'Oxygen Supply': oxygen_supply,
        'Ventilator Usage': ventilator_usage,
        'ICU Admissions': icu_admissions
    })
    
    # Create correlation heatmap
    plt.figure(figsize=(8, 6))
    correlation_matrix = data.corr()
    
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, fmt='.3f', cbar_kws={'shrink': 0.8})
    
    plt.title('HUTANO Hospital Resource Correlation Matrix\nOxygen, Ventilators, and ICU Admissions', 
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('hutano_resource_correlation_matrix.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generated: hutano_resource_correlation_matrix.png")
    
    return correlation_matrix

if __name__ == "__main__":
    print("Generating HUTANO Oxygen Supply vs ICU Admissions Correlation...")
    print("=" * 60)
    
    try:
        # Generate main correlation plot
        corr_coef, p_val = generate_oxygen_icu_correlation()
        
        # Generate enhanced analysis
        corr_matrix = generate_enhanced_correlation_analysis()
        
        print("=" * 60)
        print("Correlation analysis completed successfully!")
        print("\nGenerated files:")
        print("- hutano_oxygen_icu_correlation.png - Scatter plot with correlation")
        print("- hutano_resource_correlation_matrix.png - Multi-variable correlation heatmap")
        print("- hutano_oxygen_icu_data.csv - Raw data for analysis")
        print(f"\nKey findings:")
        print(f"- Oxygen Supply vs ICU Admissions correlation: {corr_coef:.3f}")
        print(f"- Statistical significance (p-value): {p_val:.3f}")
        
        if p_val < 0.05:
            print("- Correlation is statistically significant (p < 0.05)")
        else:
            print("- Correlation is not statistically significant (p >= 0.05)")
            
    except Exception as e:
        print(f"Error generating correlation analysis: {e}")
