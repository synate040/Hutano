"""
HUTANO Hospital Resource Forecasting System - Data Preprocessing Examples
Code snippets for feature engineering, missing value handling, and data sampling
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Set style for professional plots
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def generate_sample_hospital_data():
    """Generate sample hospital data for demonstration"""
    np.random.seed(42)
    
    n_samples = 1000
    
    # Generate base hospital data
    data = {
        'hospital_id': np.random.choice(['H001', 'H002', 'H003', 'H004'], n_samples),
        'date': pd.date_range('2025-01-01', periods=n_samples, freq='D'),
        'admissions': np.random.poisson(50, n_samples),
        'bed_occupancy': np.random.uniform(0.4, 0.95, n_samples),
        'icu_beds_available': np.random.randint(5, 25, n_samples),
        'length_of_stay': np.random.exponential(4, n_samples),
        'disease_type': np.random.choice(['Malaria', 'Pneumonia', 'Diabetes', 'Hypertension', 'Other'], n_samples),
        'oxygen_supply': np.random.uniform(80, 100, n_samples),
        'staff_count': np.random.randint(20, 80, n_samples),
        'emergency_cases': np.random.poisson(8, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce missing values for demonstration
    missing_indices = np.random.choice(df.index, size=int(0.15 * len(df)), replace=False)
    df.loc[missing_indices[:50], 'oxygen_supply'] = np.nan
    df.loc[missing_indices[50:100], 'length_of_stay'] = np.nan
    df.loc[missing_indices[100:150], 'staff_count'] = np.nan
    
    return df

def feature_engineering_examples():
    """Demonstrate feature engineering techniques for HUTANO system"""
    
    print("=" * 60)
    print("FEATURE ENGINEERING FOR HUTANO SYSTEM")
    print("=" * 60)
    
    # Generate sample data
    df = generate_sample_hospital_data()
    
    print("\n1. TEMPORAL FEATURE ENGINEERING")
    print("-" * 40)
    
    # Extracting temporal features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['quarter'] = df['date'].dt.quarter
    df['day_of_year'] = df['date'].dt.dayofyear
    
    print("# Temporal Feature Engineering")
    print("df['year'] = df['date'].dt.year")
    print("df['month'] = df['date'].dt.month")
    print("df['day_of_week'] = df['date'].dt.dayofweek")
    print("df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)")
    print("df['quarter'] = df['date'].dt.quarter")
    print("df['day_of_year'] = df['date'].dt.dayofyear")
    
    print(f"\nTemporal features created: {['year', 'month', 'day_of_week', 'is_weekend', 'quarter', 'day_of_year']}")
    
    print("\n2. CAPACITY UTILIZATION FEATURES")
    print("-" * 40)
    
    # Creating capacity utilization features
    df['bed_utilization_rate'] = df['bed_occupancy'] * 100
    df['icu_utilization'] = (25 - df['icu_beds_available']) / 25  # Assuming max 25 ICU beds
    df['staff_per_admission'] = df['staff_count'] / (df['admissions'] + 1)  # +1 to avoid division by zero
    df['emergency_ratio'] = df['emergency_cases'] / (df['admissions'] + 1)
    
    print("# Capacity Utilization Features")
    print("df['bed_utilization_rate'] = df['bed_occupancy'] * 100")
    print("df['icu_utilization'] = (25 - df['icu_beds_available']) / 25")
    print("df['staff_per_admission'] = df['staff_count'] / (df['admissions'] + 1)")
    print("df['emergency_ratio'] = df['emergency_cases'] / (df['admissions'] + 1)")
    
    print("\n3. CATEGORICAL ENCODING")
    print("-" * 40)
    
    # Labeling encoding for ordinal features
    le_hospital = LabelEncoder()
    df['hospital_encoded'] = le_hospital.fit_transform(df['hospital_id'])
    
    # One-hot encoding for disease types
    disease_dummies = pd.get_dummies(df['disease_type'], prefix='disease')
    df = pd.concat([df, disease_dummies], axis=1)
    
    print("# Categorical Encoding")
    print("from sklearn.preprocessing import LabelEncoder")
    print("le_hospital = LabelEncoder()")
    print("df['hospital_encoded'] = le_hospital.fit_transform(df['hospital_id'])")
    print("")
    print("# One-hot encoding for disease types")
    print("disease_dummies = pd.get_dummies(df['disease_type'], prefix='disease')")
    print("df = pd.concat([df, disease_dummies], axis=1)")
    
    print("\n4. INTERACTION FEATURES")
    print("-" * 40)
    
    # Create interaction features
    df['occupancy_x_admissions'] = df['bed_occupancy'] * df['admissions']
    df['staff_efficiency'] = df['admissions'] / df['staff_count']
    df['resource_pressure'] = df['bed_occupancy'] * df['icu_utilization']
    
    print("# Interaction Features")
    print("df['occupancy_x_admissions'] = df['bed_occupancy'] * df['admissions']")
    print("df['staff_efficiency'] = df['admissions'] / df['staff_count']")
    print("df['resource_pressure'] = df['bed_occupancy'] * df['icu_utilization']")
    
    print("\n5. ROLLING WINDOW FEATURES")
    print("-" * 40)
    
    # Sort by date for rolling features
    df = df.sort_values('date')
    
    # Create rolling features
    df['admissions_7day_avg'] = df.groupby('hospital_id')['admissions'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
    df['occupancy_7day_avg'] = df.groupby('hospital_id')['bed_occupancy'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
    df['admissions_trend'] = df.groupby('hospital_id')['admissions'].pct_change(periods=7).fillna(0)
    
    print("# Rolling Window Features")
    print("df = df.sort_values('date')")
    print("df['admissions_7day_avg'] = df.groupby('hospital_id')['admissions'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)")
    print("df['occupancy_7day_avg'] = df.groupby('hospital_id')['bed_occupancy'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)")
    print("df['admissions_trend'] = df.groupby('hospital_id')['admissions'].pct_change(periods=7).fillna(0)")
    
    print(f"\nTotal features after engineering: {len(df.columns)}")
    print(f"Original features: {len(generate_sample_hospital_data().columns)}")
    print(f"New features created: {len(df.columns) - len(generate_sample_hospital_data().columns)}")
    
    return df

def missing_value_handling_examples():
    """Demonstrate missing value handling techniques"""
    
    print("\n" + "=" * 60)
    print("MISSING VALUE HANDLING FOR HUTANO SYSTEM")
    print("=" * 60)
    
    # Generate data with missing values
    df = generate_sample_hospital_data()
    
    print("\n1. MISSING VALUE ANALYSIS")
    print("-" * 40)
    
    # Checking missing values
    missing_info = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    
    print("# Missing Value Analysis")
    print("missing_info = df.isnull().sum()")
    print("missing_percent = (df.isnull().sum() / len(df)) * 100")
    print("")
    print("missing_summary = pd.DataFrame({")
    print("    'Missing_Count': missing_info,")
    print("    'Missing_Percentage': missing_percent")
    print("})")
    
    print(f"\nMissing values found in:")
    for col in missing_info[missing_info > 0].index:
        print(f"- {col}: {missing_info[col]} values ({missing_percent[col]:.1f}%)")
    
    print("\n2. SIMPLE IMPUTATION METHODS")
    print("-" * 40)
    
    # Simple imputation
    print("# Mean imputation for numerical features")
    print("from sklearn.impute import SimpleImputer")
    print("mean_imputer = SimpleImputer(strategy='mean')")
    print("df['oxygen_supply_mean'] = mean_imputer.fit_transform(df[['oxygen_supply']]).flatten()")
    
    mean_imputer = SimpleImputer(strategy='mean')
    df['oxygen_supply_mean'] = mean_imputer.fit_transform(df[['oxygen_supply']]).flatten()
    
    print("\n# Median imputation for skewed features")
    print("median_imputer = SimpleImputer(strategy='median')")
    print("df['length_of_stay_median'] = median_imputer.fit_transform(df[['length_of_stay']]).flatten()")
    
    median_imputer = SimpleImputer(strategy='median')
    df['length_of_stay_median'] = median_imputer.fit_transform(df[['length_of_stay']]).flatten()
    
    print("\n# Mode imputation for categorical features")
    print("mode_imputer = SimpleImputer(strategy='most_frequent')")
    print("df['staff_count_mode'] = mode_imputer.fit_transform(df[['staff_count']]).flatten()")
    
    mode_imputer = SimpleImputer(strategy='most_frequent')
    df['staff_count_mode'] = mode_imputer.fit_transform(df[['staff_count']]).flatten()
    
    print("\n3. ADVANCED IMPUTATION METHODS")
    print("-" * 40)
    
    # KNN imputation
    print("# KNN Imputation")
    print("from sklearn.impute import KNNImputer")
    print("knn_imputer = KNNImputer(n_neighbors=5)")
    print("numerical_cols = ['admissions', 'bed_occupancy', 'icu_beds_available', 'oxygen_supply', 'staff_count']")
    print("df_knn = pd.DataFrame(knn_imputer.fit_transform(df[numerical_cols]), columns=numerical_cols)")
    
    numerical_cols = ['admissions', 'bed_occupancy', 'icu_beds_available', 'oxygen_supply', 'staff_count']
    knn_imputer = KNNImputer(n_neighbors=5)
    df_knn = pd.DataFrame(knn_imputer.fit_transform(df[numerical_cols]), columns=numerical_cols)
    
    print("\n4. FORWARD FILL FOR TIME SERIES")
    print("-" * 40)
    
    # Forward fill for time series
    print("# Forward fill for time series data")
    print("df_sorted = df.sort_values(['hospital_id', 'date'])")
    print("df_sorted['oxygen_supply_ffill'] = df_sorted.groupby('hospital_id')['oxygen_supply'].fillna(method='ffill')")
    print("df_sorted['oxygen_supply_bfill'] = df_sorted.groupby('hospital_id')['oxygen_supply_ffill'].fillna(method='bfill')")
    
    df_sorted = df.sort_values(['hospital_id', 'date'])
    df_sorted['oxygen_supply_ffill'] = df_sorted.groupby('hospital_id')['oxygen_supply'].fillna(method='ffill')
    df_sorted['oxygen_supply_bfill'] = df_sorted.groupby('hospital_id')['oxygen_supply_ffill'].fillna(method='bfill')
    
    return df, df_knn

def create_data_sampling_visualization():
    """Create pie chart for data sampling distribution"""
    
    print("\n" + "=" * 60)
    print("DATA SAMPLING VISUALIZATION")
    print("=" * 60)
    
    # Generate sample data
    df = generate_sample_hospital_data()
    
    # Create train-test split
    X = df.drop(['date'], axis=1)  # Features
    y = df['admissions']  # Target variable
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=df['hospital_id'])
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)  # 0.25 * 0.8 = 0.2
    
    print("\n1. DATA SPLITTING CODE")
    print("-" * 40)
    print("# Train-Validation-Test Split")
    print("from sklearn.model_selection import train_test_split")
    print("")
    print("X = df.drop(['date'], axis=1)  # Features")
    print("y = df['admissions']  # Target variable")
    print("")
    print("# First split: 80% train+val, 20% test")
    print("X_train, X_test, y_train, y_test = train_test_split(")
    print("    X, y, test_size=0.2, random_state=42, stratify=df['hospital_id'])")
    print("")
    print("# Second split: 60% train, 20% validation")
    print("X_train, X_val, y_train, y_val = train_test_split(")
    print("    X_train, y_train, test_size=0.25, random_state=42)")
    
    # Calculate sample sizes
    total_samples = len(df)
    train_samples = len(X_train)
    val_samples = len(X_val)
    test_samples = len(X_test)
    
    print(f"\nDataset Distribution:")
    print(f"- Total samples: {total_samples}")
    print(f"- Training set: {train_samples} ({train_samples/total_samples*100:.1f}%)")
    print(f"- Validation set: {val_samples} ({val_samples/total_samples*100:.1f}%)")
    print(f"- Test set: {test_samples} ({test_samples/total_samples*100:.1f}%)")
    
    # Create pie chart
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.patch.set_facecolor('white')
    
    # Panel 1: Data split pie chart
    sizes = [train_samples, val_samples, test_samples]
    labels = ['Training\n(60%)', 'Validation\n(20%)', 'Test\n(20%)']
    colors = ['#4472C4', '#70AD47', '#FFC000']
    explode = (0.05, 0.05, 0.05)
    
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                      startangle=90, explode=explode, shadow=True)
    ax1.set_title('HUTANO: Data Sampling Distribution', fontweight='bold', fontsize=14)
    
    # Panel 2: Hospital distribution
    hospital_counts = df['hospital_id'].value_counts()
    ax2.pie(hospital_counts.values, labels=hospital_counts.index, autopct='%1.1f%%',
           colors=['#2E8B8B', '#DAA520', '#E74C3C', '#9B59B6'], startangle=90)
    ax2.set_title('Hospital Distribution', fontweight='bold', fontsize=14)
    
    # Panel 3: Disease type distribution
    disease_counts = df['disease_type'].value_counts()
    ax3.pie(disease_counts.values, labels=disease_counts.index, autopct='%1.1f%%',
           colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'], startangle=90)
    ax3.set_title('Disease Type Distribution', fontweight='bold', fontsize=14)
    
    # Panel 4: Missing data distribution
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]
    if len(missing_data) > 0:
        ax4.pie(missing_data.values, labels=missing_data.index, autopct='%1.1f%%',
               colors=['#FF9999', '#66B2FF', '#99FF99'], startangle=90)
        ax4.set_title('Missing Data Distribution', fontweight='bold', fontsize=14)
    else:
        ax4.text(0.5, 0.5, 'No Missing Data', ha='center', va='center', fontsize=16, fontweight='bold')
        ax4.set_title('Missing Data Distribution', fontweight='bold', fontsize=14)
    
    fig.suptitle('HUTANO: Comprehensive Data Analysis Dashboard', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('hutano_data_sampling_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("\nGenerated: hutano_data_sampling_analysis.png")
    
    return {
        'total': total_samples,
        'train': train_samples,
        'validation': val_samples,
        'test': test_samples
    }

if __name__ == "__main__":
    print("HUTANO HOSPITAL RESOURCE FORECASTING SYSTEM")
    print("Data Preprocessing and Analysis Examples")
    print("=" * 80)
    
    try:
        # Run feature engineering examples
        df_engineered = feature_engineering_examples()
        
        # Run missing value handling examples
        df_original, df_imputed = missing_value_handling_examples()
        
        # Create data sampling visualization
        sampling_info = create_data_sampling_visualization()
        
        print("\n" + "=" * 80)
        print("PREPROCESSING COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nGenerated Files:")
        print("- hutano_data_sampling_analysis.png - Comprehensive data analysis dashboard")
        
        print("\nCode Examples Demonstrated:")
        print("1. Feature Engineering:")
        print("   - Temporal features (year, month, day_of_week, etc.)")
        print("   - Capacity utilization features")
        print("   - Categorical encoding (Label encoding, One-hot encoding)")
        print("   - Interaction features")
        print("   - Rolling window features")
        
        print("\n2. Missing Value Handling:")
        print("   - Simple imputation (mean, median, mode)")
        print("   - KNN imputation")
        print("   - Forward/backward fill for time series")
        print("   - Missing value analysis")
        
        print("\n3. Data Sampling:")
        print("   - Train-validation-test split (60%-20%-20%)")
        print("   - Stratified sampling by hospital")
        print("   - Distribution visualizations")
        
        print(f"\nFinal Dataset Statistics:")
        print(f"- Original features: 10")
        print(f"- Engineered features: {len(df_engineered.columns)}")
        print(f"- Training samples: {sampling_info['train']}")
        print(f"- Validation samples: {sampling_info['validation']}")
        print(f"- Test samples: {sampling_info['test']}")
        
    except Exception as e:
        print(f"Error in preprocessing: {e}")
