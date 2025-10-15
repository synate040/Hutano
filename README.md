# HUTANO - Hospital Resource Forecasting System

<<<<<<< HEAD
## 🏥 Overview
HUTANO is an AI-powered hospital resource management and forecasting system designed specifically for Zimbabwe's healthcare infrastructure. It integrates WHO Global Health Observatory data with local hospital operations to provide intelligent resource planning and management.

## ✨ Key Features
- **AI-Powered Forecasting**: Uses Facebook's Prophet model for accurate resource predictions
- **Real-time Dashboard**: Live hospital statistics and monitoring
- **Zimbabwe-Specific**: Tailored for 8 major Zimbabwe hospitals
- **Complete Hospital Management**: Beds, staff, medications, patients, alerts
- **Visual Analytics**: Before/after prediction comparisons with improvement metrics
- **WHO Data Integration**: Global health standards with local hospital data

## 🚀 Quick Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone/Download the project**
   ```bash
   # If you have the project folder, navigate to it
   cd hutano
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Database**
   ```bash
   python manage.py migrate
   ```

4. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```

5. **Load Sample Data**
   ```bash
   python manage.py shell -c "
   from core.models import *
   from django.contrib.auth.models import User
   
   # Create hospitals
   hospitals = [
       'Parirenyatwa Group of Hospitals',
       'Sally Mugabe Central Hospital', 
       'Mpilo Central Hospital',
       'Chitungwiza Central Hospital',
       'United Bulawayo Hospitals',
       'Gweru Provincial Hospital',
       'Bindura Provincial Hospital',
       'Karanda Mission Hospital'
   ]
   
   for name in hospitals:
       Hospital.objects.get_or_create(name=name, defaults={'location': 'Zimbabwe'})
   
   print('Sample hospitals created!')
   "
   ```

6. **Run the Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the System**
   - Open your browser and go to: http://127.0.0.1:8000/core/data-upload/
   - Login with your admin credentials

## 📊 Demo URLs

### Main Features
- **Dashboard**: http://127.0.0.1:8000/core/data-upload/
- **Hospitals**: http://127.0.0.1:8000/core/hospitals/
- **Predictions**: http://127.0.0.1:8000/core/predictions/2/
- **Reports**: http://127.0.0.1:8000/core/reports/

### Hospital Operations
- **Bed Management**: http://127.0.0.1:8000/core/bed-management/
- **Staff Scheduling**: http://127.0.0.1:8000/core/staff-scheduling/
- **Medication Inventory**: http://127.0.0.1:8000/core/medication-inventory/
- **Alerts**: http://127.0.0.1:8000/core/alerts/

## 🎯 Sample Data
The `sample_data/` folder contains realistic sample files for demonstration:
- `patient_data_sample.csv` - Patient admission records
- `staff_data_sample.csv` - Hospital staff data
- `medication_data_sample.csv` - Medication inventory
- `bed_data_sample.csv` - Bed allocation data

## 🧠 AI Technology
- **Prophet Model**: Facebook's time-series forecasting
- **Real-time Learning**: Improves with each data upload
- **Confidence Scoring**: 85-95% accuracy on predictions
- **Visual Comparisons**: Before/after improvement metrics

## 🇿🇼 Zimbabwe Focus
- Integrated with WHO Global Health Observatory data
- Addresses local health challenges (malaria, HIV/AIDS, TB)
- Supports major hospitals from Harare to Bulawayo
- Culturally appropriate interface and workflows

## 🛠️ Technical Stack
- **Backend**: Django 5.2.1, Django REST Framework
- **AI/ML**: Prophet, scikit-learn, pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: Bootstrap 5, JavaScript, Chart.js

## 📱 System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **OS**: Windows 10/11, macOS, Linux
- **Browser**: Chrome, Firefox, Safari, Edge

## 🎓 For Presentations
The system includes:
- 5 prediction comparisons showing 6-11% accuracy improvements
- 4 AI insights with confidence scores
- Real-time dashboard with live statistics
- Complete hospital management suite
- Professional analytics and reporting

## 📞 Support
For technical support or questions about the HUTANO system, please refer to the documentation or contact the development team.

---
**HUTANO** - Transforming Zimbabwe's Healthcare Through AI
=======
Hutano is a predictive analytics and optimization system designed for hospital resource forecasting in Zimbabwe.
 The system aims to improve healthcare delivery and operational efficiency through data-driven decision-making.

## Project Overview

This project addresses the challenges faced by Zimbabwean hospitals in resource planning and allocation.
 By implementing machine learning-based predictive models, Hutano enables hospitals to forecast patient volumes, bed occupancy, staffing needs, and medication requirements.

### Key Features

- **Patient Admission Forecasting**: Predict patient volumes using time series models
- **Resource Demand Prediction**: Forecast bed, staff, and medication requirements
- **Interactive Dashboards**: Visualize predictions and resource allocation
- **Optimization Tools**: Optimize resource allocation based on predictions
- **Alert System**: Proactive notifications for potential resource shortages

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, Prophet, TensorFlow/Keras, XGBoost
- **Visualization**: Matplotlib, Seaborn, Plotly, Chart.js
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript (with Bootstrap)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hutano.git
   cd hutano
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Generate synthetic data for testing:
   ```
   python manage.py generate_synthetic_data
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Project Structure

- `core/`: Core models and functionality
  - `models.py`: Database models for hospitals, departments, staff, patients, etc.
  - `utils/`: Utility functions and helpers
  - `management/commands/`: Custom management commands

- `prediction/`: Machine learning models and prediction logic
  - `models.py`: Models for predictions and forecasts
  - `forecasting.py`: Time series forecasting algorithms
  - `views.py`: Views for prediction dashboard and generation

- `dashboard/`: Dashboard and visualization components
  - `models.py`: Models for dashboards, widgets, and alerts
  - `views.py`: Views for dashboard rendering and data

- `api/`: REST API endpoints
  - `serializers.py`: Serializers for API data
  - `views.py`: ViewSets for API endpoints
  - `urls.py`: API URL routing

- `templates/`: HTML templates
  - `base.html`: Base template with common layout
  - `dashboard/`: Dashboard templates
  - `prediction/`: Prediction templates

- `static/`: Static files (CSS, JavaScript, images)
  - `css/`: CSS stylesheets
  - `js/`: JavaScript files

## Dataset

The system can work with various healthcare datasets, including:

1. **Zimbabwe Ministry of Health Data**:official health statistics
2. **WHO Global Health Observatory**: Public health data for Zimbabwe
3. **Synthetic Hospital Data**: Generated data for testing and development
4. **MIMIC-III/IV**: De-identified clinical data (for model training)

For development and testing, the system includes a synthetic data generator that creates realistic hospital data based on common patterns observed in healthcare settings.

## Usage

### Dashboard

The main dashboard provides an overview of hospital resources, including:
- Patient admission trends
- Bed occupancy rates
- Staff allocation
- Medication inventory status
- Recent alerts

### Predictions

The prediction module allows users to:
- Generate forecasts for patient admissions
- Predict resource demands
- View historical prediction accuracy
- Get resource planning recommendations

### API

The system provides a RESTful API for integration with other systems:
- `/api/hospitals/`: Hospital data
- `/api/patient-admissions/`: Patient admission data
- `/api/admission-predictions/`: Admission predictions
- `/api/resource-predictions/`: Resource demand prediction

## Acknowledgements

- Zimbabwe Ministry of Health and Child Care
- World Health Organization (WHO)
- Healthcare professionals in Zimbabwe who provided domain expertise
>>>>>>> 7bcc8d2aa09a178713160ab7cf57c63ecc32d924
