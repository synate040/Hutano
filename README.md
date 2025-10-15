# HUTANO - Hospital Resource Forecasting System

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
