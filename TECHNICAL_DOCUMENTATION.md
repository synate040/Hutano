# HUTANO - Technical Documentation

## 🛠️ System Architecture

### Technology Stack
- **Backend**: Django 4.2 (Python)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Authentication**: Django's built-in authentication system

### Project Structure
```
hutano/
├── hutano/                 # Main project directory
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── core/                  # Core application
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py           # URL patterns
│   ├── templates/        # HTML templates
│   └── management/       # Custom management commands
├── prediction/           # Forecasting module
├── templates/           # Global templates
├── static/             # Static files (CSS, JS, images)
└── media/              # User uploaded files
```

## 📊 Database Models

### Core Models

#### Hospital
```python
class Hospital(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    bed_capacity = models.IntegerField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    established_date = models.DateField()
    hospital_type = models.CharField(max_length=50)
```

#### Staff
```python
class Staff(models.Model):
    hospital = models.ForeignKey(Hospital)
    staff_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    category = models.ForeignKey(StaffCategory)
    position = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
```

#### PatientAdmission
```python
class PatientAdmission(models.Model):
    hospital = models.ForeignKey(Hospital)
    patient_id = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(null=True, blank=True)
    diagnosis = models.CharField(max_length=200)
    is_emergency = models.BooleanField(default=False)
```

#### MedicationInventory
```python
class MedicationInventory(models.Model):
    hospital = models.ForeignKey(Hospital)
    medication = models.ForeignKey(Medication)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField()
    expiry_date = models.DateField()
    batch_number = models.CharField(max_length=50)
```

#### BedAllocation
```python
class BedAllocation(models.Model):
    hospital = models.ForeignKey(Hospital)
    bed_number = models.CharField(max_length=20)
    bed_type = models.CharField(max_length=50)
    department = models.ForeignKey(Department)
    status = models.CharField(max_length=20)
```

## 🔧 Key Features Implementation

### 1. Hospital Comparison Dashboard
**File**: `core/views.py` - `comparison_dashboard()`

```python
def comparison_dashboard(request):
    hospitals = Hospital.objects.all()
    comparison_data = []
    
    for hospital in hospitals:
        # Calculate bed statistics
        bed_stats = calculate_bed_statistics(hospital)
        
        # Calculate patient statistics
        patient_stats = calculate_patient_statistics(hospital)
        
        # Calculate staff statistics
        staff_stats = calculate_staff_statistics(hospital)
        
        # Calculate medication statistics
        medication_stats = calculate_medication_statistics(hospital)
        
        comparison_data.append({
            'hospital': hospital,
            'bed_stats': bed_stats,
            'patient_stats': patient_stats,
            'staff_stats': staff_stats,
            'medication_stats': medication_stats,
        })
    
    return render(request, 'core/comparison_dashboard.html', {
        'comparison_data': comparison_data,
        'system_totals': calculate_system_totals(hospitals)
    })
```

### 2. Alert System
**File**: `core/views.py` - `alerts_view()`

```python
def alerts_view(request):
    alerts = []
    
    # Low stock medications
    low_stock_meds = MedicationInventory.objects.filter(
        quantity__lte=F('reorder_level')
    )
    
    # Expired medications
    expired_meds = MedicationInventory.objects.filter(
        expiry_date__lt=timezone.now().date()
    )
    
    # High bed occupancy
    high_occupancy_hospitals = []
    for hospital in Hospital.objects.all():
        occupancy_rate = calculate_occupancy_rate(hospital)
        if occupancy_rate > 90:
            high_occupancy_hospitals.append({
                'hospital': hospital,
                'occupancy_rate': occupancy_rate
            })
    
    return render(request, 'core/alerts.html', {
        'low_stock_medications': low_stock_meds,
        'expired_medications': expired_meds,
        'high_occupancy_hospitals': high_occupancy_hospitals,
    })
```

### 3. Data Population Commands

#### Real Hospital Data Command
**File**: `core/management/commands/update_real_hospital_data.py`

```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        real_hospital_data = {
            'Parirenyatwa Group of Hospitals': {
                'bed_capacity': 1200,
                'staff_count': 2500,
                'specialties': ['Cardiology', 'Neurology', 'Oncology'],
                'established': 1962,
                'type': 'Central Referral',
            },
            # ... other hospitals
        }
        
        for hospital in Hospital.objects.all():
            if hospital.name in real_hospital_data:
                data = real_hospital_data[hospital.name]
                hospital.bed_capacity = data['bed_capacity']
                hospital.save()
                
                self.create_realistic_staff(hospital, data['staff_count'])
```

#### Zimbabwe Health Data Command
**File**: `core/management/commands/add_realistic_health_data.py`

```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Zimbabwe health conditions with prevalence rates
        zimbabwe_health_conditions = {
            'Malaria': {'prevalence': 0.25, 'age_groups': [0, 5, 15, 45]},
            'HIV/AIDS': {'prevalence': 0.12, 'age_groups': [15, 25, 35, 45]},
            'Tuberculosis': {'prevalence': 0.08, 'age_groups': [15, 25, 35, 45, 55]},
            # ... other conditions
        }
        
        # EDLIZ essential medicines
        zimbabwe_essential_medicines = [
            ('Artemether/Lumefantrine (Coartem)', 'Antimalarials', 'Tablets'),
            ('Cotrimoxazole', 'Antibiotics', 'Tablets'),
            # ... other medicines
        ]
        
        self.create_essential_medicines(zimbabwe_essential_medicines)
        
        for hospital in Hospital.objects.all():
            self.generate_realistic_patients(hospital, zimbabwe_health_conditions)
```

## 🎨 Frontend Implementation

### Bootstrap 5 Integration
**File**: `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}HUTANO - Hospital Resource Management{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
```

### Chart.js Implementation
**File**: `core/templates/core/comparison_dashboard.html`

```javascript
const comparisonChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: hospitalNames,
        datasets: [{
            label: 'Occupancy Rate (%)',
            data: occupancyRates,
            backgroundColor: occupancyRates.map(rate => 
                rate > 90 ? 'rgba(220, 53, 69, 0.8)' : 
                rate > 80 ? 'rgba(255, 193, 7, 0.8)' : 
                'rgba(25, 135, 84, 0.8)'
            ),
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                max: 100,
                title: {
                    display: true,
                    text: 'Occupancy Rate (%)'
                }
            }
        }
    }
});
```

## 🚀 Deployment Instructions

### Development Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hutano
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate with real data**
   ```bash
   python manage.py populate_sample_data
   python manage.py update_real_hospital_data
   python manage.py add_realistic_health_data
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Production Deployment
1. **Environment Variables**
   ```bash
   export DEBUG=False
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='postgresql://user:pass@localhost/hutano'
   ```

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **WSGI Configuration**
   - Use Gunicorn or uWSGI
   - Configure Nginx for static files
   - Set up SSL certificates

## 📊 Performance Optimization

### Database Optimization
- **Indexes** on frequently queried fields
- **Select_related** and **prefetch_related** for foreign keys
- **Database connection pooling**
- **Query optimization** for dashboard views

### Caching Strategy
- **Redis** for session storage
- **Template caching** for static content
- **Database query caching** for expensive operations
- **CDN** for static assets

### Security Measures
- **CSRF protection** enabled
- **SQL injection** prevention through ORM
- **XSS protection** with template escaping
- **HTTPS** enforcement in production
- **Rate limiting** for API endpoints

## 🧪 Testing

### Unit Tests
```python
class HospitalModelTest(TestCase):
    def test_hospital_creation(self):
        hospital = Hospital.objects.create(
            name="Test Hospital",
            location="Test Location",
            bed_capacity=100
        )
        self.assertEqual(hospital.name, "Test Hospital")
        self.assertEqual(hospital.bed_capacity, 100)
```

### Integration Tests
```python
class ComparisonDashboardTest(TestCase):
    def test_comparison_dashboard_view(self):
        response = self.client.get('/core/comparison/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hospital Comparison Dashboard')
```

## 📈 Monitoring & Analytics

### System Metrics
- **Response time** monitoring
- **Database query** performance
- **Memory usage** tracking
- **Error rate** monitoring

### Business Metrics
- **Hospital occupancy** rates
- **Staff utilization** metrics
- **Medication stock** levels
- **Patient flow** analytics

---

**This technical documentation provides a comprehensive overview of the HUTANO system architecture, implementation details, and deployment procedures.**
