#!/usr/bin/env python3
"""
Quick System Check for HUTANO

This script quickly verifies all system components are working.
"""

import os
import sys

def check_django():
    """Check Django setup."""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
        import django
        django.setup()
        print("✅ Django: OK")
        return True
    except Exception as e:
        print(f"❌ Django: {e}")
        return False

def check_database():
    """Check database connection."""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('SELECT 1')
        print("✅ Database: OK")
        return True
    except Exception as e:
        print(f"❌ Database: {e}")
        return False

def check_models():
    """Check if models can be imported."""
    try:
        from core.models import Hospital
        from prediction.models import PredictionModel
        print("✅ Django Models: OK")
        return True
    except Exception as e:
        print(f"❌ Django Models: {e}")
        return False

def check_ml_libraries():
    """Check ML library availability."""
    libraries = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'scikit-learn': 'sklearn',
        'XGBoost': 'xgboost',
        'matplotlib': 'matplotlib'
    }
    
    all_ok = True
    for name, module in libraries.items():
        try:
            __import__(module)
            print(f"✅ {name}: OK")
        except ImportError:
            print(f"❌ {name}: Not installed")
            all_ok = False
    
    return all_ok

def check_forecasting_modules():
    """Check our custom forecasting modules."""
    modules = [
        'prediction.xgboost_forecasting',
        'prediction.random_forest_forecasting',
        'prediction.ensemble_forecasting'
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module.split('.')[-1]}: OK")
        except ImportError as e:
            print(f"❌ {module.split('.')[-1]}: {e}")
            all_ok = False
    
    return all_ok

def check_sample_data():
    """Check if sample data file exists."""
    if os.path.exists('sample_hospital_data.csv'):
        print("✅ Sample Data: OK")
        return True
    else:
        print("❌ Sample Data: sample_hospital_data.csv not found")
        return False

def check_urls():
    """Check URL configuration."""
    try:
        from django.urls import reverse
        urls_to_check = [
            'prediction:dashboard',
            'prediction:upload_data',
        ]
        
        for url_name in urls_to_check:
            try:
                reverse(url_name)
                print(f"✅ URL {url_name}: OK")
            except:
                print(f"❌ URL {url_name}: Not found")
                return False
        
        return True
    except Exception as e:
        print(f"❌ URL Check: {e}")
        return False

def main():
    """Run all system checks."""
    print("🔍 HUTANO SYSTEM QUICK CHECK")
    print("=" * 40)
    
    checks = [
        ("Django Setup", check_django),
        ("Database Connection", check_database),
        ("Django Models", check_models),
        ("ML Libraries", check_ml_libraries),
        ("Forecasting Modules", check_forecasting_modules),
        ("Sample Data", check_sample_data),
        ("URL Configuration", check_urls),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 40)
    print("SUMMARY:")
    
    if all(results):
        print("🎉 ALL SYSTEMS GO! Your HUTANO system is ready!")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver 8000")
        print("2. Open: http://localhost:8000/prediction/")
        print("3. Upload: sample_hospital_data.csv")
        print("4. Test all 5 models!")
    else:
        print("❌ Some issues found. Please fix the errors above.")
        failed_checks = [checks[i][0] for i, result in enumerate(results) if not result]
        print(f"Failed checks: {', '.join(failed_checks)}")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
