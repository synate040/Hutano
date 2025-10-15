import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Example data structure
# Replace this with your actual data loading
data = pd.DataFrame({
    'date': pd.date_range(start='2021-01-01', periods=48, freq='ME'),
    'actual_admissions': [900 + (i % 12) * 10 + (i % 5) * 20 for i in range(48)]
})
forecast = pd.DataFrame({
    'date': pd.date_range(start='2025-01-01', periods=12, freq='ME'),
    'forecasted_admissions': [950 + (i % 6) * 15 for i in range(12)]
})

plt.figure(figsize=(10, 6))
plt.plot(data['date'], data['actual_admissions'], label='Actual Admissions')
plt.plot(forecast['date'], forecast['forecasted_admissions'], 'r--', label='Forecasted Admissions')
plt.title('Monthly Hospital Admissions – Historical Trend and Forecast')
plt.xlabel('Date')
plt.ylabel('Admissions')
plt.legend()
plt.tight_layout()
plt.savefig('monthly_hospital_admissions.png')
plt.close()

# Bed Occupancy Rate Over Time
bed_data = pd.DataFrame({
    'month': pd.date_range(start='2019-01-01', periods=48, freq='ME'),
    'bed_occupancy_rate': [60 + i*0.8 + (i % 8) * 2 for i in range(48)]
})

plt.figure(figsize=(8, 5))
plt.plot(bed_data['month'], bed_data['bed_occupancy_rate'])
plt.title('Bed Occupancy Rate Over Time')
plt.xlabel('Month')
plt.ylabel('Bed Occupancy Rate (%)')
plt.tight_layout()
plt.savefig('bed_occupancy_rate.png')
plt.close()

# Staff-to-Patient Ratio by Facility Type (synthetic data for Hutano system)
np.random.seed(42)
staff_patient_data = pd.DataFrame({
    'Facility Type': (['Urban centres'] * 30) + (['Rural districts'] * 30),
    'Staff-to-Patient Ratio': np.concatenate([
        np.random.normal(0.18, 0.04, 30),  # Urban centres
        np.random.normal(0.35, 0.15, 30)   # Rural districts
    ])
})

plt.figure(figsize=(8, 5))
sns.boxplot(x='Facility Type', y='Staff-to-Patient Ratio', data=staff_patient_data)
plt.title('Staff-to-Patient Ratio by Facility Type')
plt.xlabel('Facility Type')
plt.ylabel('Staff-to-Patient Ratio')
plt.tight_layout()
plt.savefig('staff_to_patient_ratio.png')
plt.close()

# Oxygen Supply vs ICU Admissions (synthetic data for Hutano system)
np.random.seed(123)
oxygen_supply = np.random.uniform(1, 10, 80)
# Simulate a strong positive correlation with some noise
icu_admissions = 2 * oxygen_supply + np.random.normal(0, 2, 80)

corr = np.corrcoef(oxygen_supply, icu_admissions)[0, 1]

plt.figure(figsize=(9, 6))
sns.regplot(x=oxygen_supply, y=icu_admissions, scatter_kws={'color': 'black'}, line_kws={'color': 'red', 'alpha': 0.5})
plt.title('Oxygen Supply vs ICU Admissions (Scatter)')
plt.xlabel('Oxygen Supply (cylinders/day)')
plt.ylabel('ICU Admissions')
plt.text(1.2, max(icu_admissions)-2, f'r = {corr:.2f}', fontsize=12)
plt.tight_layout()
plt.savefig('oxygen_vs_icu.png')
plt.close()