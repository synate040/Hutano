# 🚀 HUTANO Quick Demo URLs

## 🎯 **Essential Demo URLs for HUTANO System**

### **🏠 Main Dashboard**
- **URL**: `http://localhost:8000/`
- **Purpose**: System overview and main entry point

### **📤 Data Upload & Processing**
- **URL**: `http://localhost:8000/core/data-upload/`
- **Purpose**: Upload CSV files and generate AI insights
- **Demo Files**: Use files from `sample_data/` folder

### **🔮 ML Predictions & Forecasting**
- **URL**: `http://localhost:8000/prediction/`
- **Purpose**: View ML model predictions and accuracy
- **All Predictions**: `http://localhost:8000/prediction/all/?type=admissions&hospital=1`

### **📊 Advanced Analytics**

#### **🔍 Sensitivity Analysis**
- **URL**: `http://localhost:8000/core/sensitivity-analysis/`
- **Purpose**: Feature importance analysis with impact visualization
- **Highlights**: Bed Occupancy Rate (0.042 Δ MAE), color-coded categories

#### **🌡️ Correlation Analysis**
- **URL**: `http://localhost:8000/core/correlation-analysis/`
- **Purpose**: Pearson correlation heatmap of key variables
- **Highlights**: Strong correlations (-0.89 to +0.84), actionable insights

#### **📈 Comparison Dashboard**
- **URL**: `http://localhost:8000/core/comparison/`
- **Purpose**: Before/after prediction comparisons
- **Highlights**: Visual accuracy improvements

### **🚨 Operational Features**

#### **⚠️ Alerts System**
- **URL**: `http://localhost:8000/core/alerts/`
- **Purpose**: Real-time resource alerts and warnings
- **Highlights**: Proactive shortage notifications

#### **🏥 Hospital Management**
- **URL**: `http://localhost:8000/core/hospitals/`
- **Purpose**: Multi-hospital support and management
- **Highlights**: Scalability demonstration

#### **📋 Reports & Export**
- **URL**: `http://localhost:8000/core/reports/`
- **Purpose**: Professional reporting and export capabilities
- **Highlights**: CSV/Excel export functionality

### **⚙️ System Management**
- **URL**: `http://localhost:8000/core/system-settings/`
- **Purpose**: System configuration and settings

---

## 📊 **Demo Data Files (Ready for Upload)**

### **📁 Location**: `sample_data/` folder

1. **hospital_admissions_demo.csv** - 365 days of admission patterns
2. **resource_utilization_demo.csv** - Daily resource metrics
3. **patient_demographics_demo.csv** - 500 Zimbabwean patient records
4. **staff_performance_demo.csv** - Daily staff metrics
5. **medication_usage_demo.csv** - Medication inventory data

---

## 🎯 **Quick Demo Flow (15 minutes)**

### **1. System Overview (2 min)**
- Start at: `http://localhost:8000/`
- Show: Professional dashboard, Zimbabwe context

### **2. Data Upload (5 min)**
- Navigate to: `http://localhost:8000/core/data-upload/`
- Upload: `hospital_admissions_demo.csv`
- Show: AI insights generation, accuracy improvements

### **3. ML Predictions (3 min)**
- Navigate to: `http://localhost:8000/prediction/`
- Show: 5 ML models, accuracy scores (87-92%)

### **4. Advanced Analytics (3 min)**
- **Sensitivity**: `http://localhost:8000/core/sensitivity-analysis/`
- **Correlation**: `http://localhost:8000/core/correlation-analysis/`
- Show: Professional analytics, actionable insights

### **5. System Value (2 min)**
- Navigate to: `http://localhost:8000/core/alerts/`
- Show: Real-time alerts, operational benefits

---

## 🏆 **Key Demo Highlights**

### **📈 Performance Metrics**
- **92% Ensemble Model Accuracy**
- **15-25% Prediction Improvements**
- **5 ML Models**: ARIMA, Prophet, XGBoost, Random Forest, Ensemble

### **🇿🇼 Zimbabwe Context**
- **Authentic Names**: Tendai, Chipo, Sipho, Nomsa
- **Local Diseases**: Malaria, TB, HIV/AIDS, Hypertension
- **Hospital Types**: Major referral, provincial, mission

### **💡 AI Insights Examples**
- "Medication X low in stock - reorder immediately"
- "Bed occupancy approaching 95% - prepare overflow"
- "Predicted 20% increase in admissions next week"

### **🔧 Technical Features**
- **Real-time Processing**: Immediate insight generation
- **Professional Interface**: Production-ready design
- **Export Capabilities**: CSV/Excel downloads
- **Multi-hospital Support**: Scalable architecture

---

## 🚀 **Quick Start Commands**

### **Start Server**
```bash
cd hutano
python manage.py runserver 8000
```

### **Reset Demo Data**
```bash
cd hutano
python simple_demo_data.py
```

### **Access System**
```
Main URL: http://localhost:8000/
Demo Data: Upload files from sample_data/ folder
```

---

## 📞 **Demo Support**

### **Common Issues**
- **404 Errors**: Ensure URLs include `/core/` prefix
- **Upload Errors**: Check CSV file format and size
- **Missing Data**: Run `python simple_demo_data.py`

### **Best Practices**
- **Start with data upload** to show AI capabilities
- **Highlight accuracy improvements** (15-25%)
- **Show Zimbabwe context** with authentic names/diseases
- **Demonstrate export features** for integration

---

**🎯 This quick reference ensures smooth, professional HUTANO system demonstrations!**
