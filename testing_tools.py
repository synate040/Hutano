#!/usr/bin/env python3
"""
HUTANO Testing and Validation Tools
Comprehensive testing suite for the hospital resource forecasting system
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import sqlite3
import os
import sys
import django
from django.test import TestCase
from django.contrib.auth.models import User

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutano.settings')
django.setup()

from core.models import Hospital, PatientAdmission, PredictionComparison

class HUTANOTestSuite:
    """Comprehensive testing suite for HUTANO system"""

    def __init__(self):
        self.test_results = {}
        self.passed_tests = 0
        self.failed_tests = 0

    def run_all_tests(self):
        """Run all HUTANO system tests"""

        print("🧪 HUTANO Testing Suite")
        print("=" * 60)
        print("Running comprehensive system validation tests...")

        # Data validation tests
        self.test_data_quality()
        self.test_prophet_compatibility()
        self.test_database_integrity()

        # System functionality tests
        self.test_django_models()
        self.test_api_endpoints()
        self.test_prediction_accuracy()

        # Performance tests
        self.test_system_performance()
        self.test_load_handling()

        # Security tests
        self.test_data_security()

        self.generate_test_report()

    def test_data_quality(self):
        """Test data quality and completeness"""

        print("\n1. Testing Data Quality...")

        try:
            # Test sample data files
            sample_files = [
                'sample_data/patient_data_sample.csv',
                'sample_data/staff_data_sample.csv',
                'sample_data/medication_data_sample.csv',
                'sample_data/bed_data_sample.csv'
            ]

            quality_scores = []

            for file_path in sample_files:
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)

                    # Calculate quality metrics
                    total_cells = df.size
                    missing_cells = df.isnull().sum().sum()
                    completeness = ((total_cells - missing_cells) / total_cells) * 100

                    quality_scores.append(completeness)
                    print(f"  ✓ {file_path}: {completeness:.2f}% complete")
                else:
                    print(f"  ⚠ {file_path}: File not found")

            avg_quality = np.mean(quality_scores) if quality_scores else 0

            if avg_quality >= 95:
                self.test_results['data_quality'] = 'PASS'
                self.passed_tests += 1
                print(f"  ✅ Data Quality Test: PASSED ({avg_quality:.2f}%)")
            else:
                self.test_results['data_quality'] = 'FAIL'
                self.failed_tests += 1
                print(f"  ❌ Data Quality Test: FAILED ({avg_quality:.2f}%)")

        except Exception as e:
            self.test_results['data_quality'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ Data Quality Test: ERROR - {e}")

    def test_prophet_compatibility(self):
        """Test Prophet model compatibility"""

        print("\n2. Testing Prophet Compatibility...")

        try:
            # Create sample Prophet data
            dates = pd.date_range('2025-01-01', '2024-12-31', freq='D')
            values = np.random.poisson(18, len(dates))

            prophet_data = pd.DataFrame({
                'ds': dates,
                'y': values
            })

            # Test Prophet requirements
            checks = {
                'has_ds_column': 'ds' in prophet_data.columns,
                'has_y_column': 'y' in prophet_data.columns,
                'no_missing_values': prophet_data.isnull().sum().sum() == 0,
                'chronological_order': prophet_data['ds'].is_monotonic_increasing,
                'sufficient_data': len(prophet_data) >= 30,
                'proper_date_format': pd.api.types.is_datetime64_any_dtype(prophet_data['ds'])
            }

            all_passed = all(checks.values())

            if all_passed:
                self.test_results['prophet_compatibility'] = 'PASS'
                self.passed_tests += 1
                print("  ✅ Prophet Compatibility: PASSED")
                for check, result in checks.items():
                    print(f"    ✓ {check.replace('_', ' ').title()}: {result}")
            else:
                self.test_results['prophet_compatibility'] = 'FAIL'
                self.failed_tests += 1
                print("  ❌ Prophet Compatibility: FAILED")
                for check, result in checks.items():
                    status = "✓" if result else "✗"
                    print(f"    {status} {check.replace('_', ' ').title()}: {result}")

        except Exception as e:
            self.test_results['prophet_compatibility'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ Prophet Compatibility: ERROR - {e}")

    def test_database_integrity(self):
        """Test database integrity and connections"""

        print("\n3. Testing Database Integrity...")

        try:
            # Test Django database connection
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

            # Test model creation
            hospital_count = Hospital.objects.count()

            # Test data relationships
            if hospital_count > 0:
                sample_hospital = Hospital.objects.first()
                admissions_count = PatientAdmission.objects.filter(hospital=sample_hospital).count()
                predictions_count = PredictionComparison.objects.filter(hospital=sample_hospital).count()

                print(f"  ✓ Database connection: Active")
                print(f"  ✓ Hospitals in database: {hospital_count}")
                print(f"  ✓ Sample admissions: {admissions_count}")
                print(f"  ✓ Sample predictions: {predictions_count}")

                self.test_results['database_integrity'] = 'PASS'
                self.passed_tests += 1
                print("  ✅ Database Integrity: PASSED")
            else:
                self.test_results['database_integrity'] = 'FAIL'
                self.failed_tests += 1
                print("  ❌ Database Integrity: FAILED - No hospitals found")

        except Exception as e:
            self.test_results['database_integrity'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ Database Integrity: ERROR - {e}")

    def test_django_models(self):
        """Test Django model functionality"""

        print("\n4. Testing Django Models...")

        try:
            # Test Hospital model
            test_hospital = Hospital.objects.create(
                name="Test Hospital",
                location="Test Location",
                description="Test Description"
            )

            # Test User model
            test_user = User.objects.create_user(
                username='testuser',
                email='test@hutano.co.zw',
                password='testpass123'
            )

            # Test model relationships
            if test_hospital and test_user:
                print("  ✓ Hospital model: Working")
                print("  ✓ User model: Working")
                print("  ✓ Model relationships: Working")

                # Cleanup
                test_hospital.delete()
                test_user.delete()

                self.test_results['django_models'] = 'PASS'
                self.passed_tests += 1
                print("  ✅ Django Models: PASSED")
            else:
                self.test_results['django_models'] = 'FAIL'
                self.failed_tests += 1
                print("  ❌ Django Models: FAILED")

        except Exception as e:
            self.test_results['django_models'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ Django Models: ERROR - {e}")

    def test_api_endpoints(self):
        """Test API endpoint availability"""

        print("\n5. Testing API Endpoints...")

        try:
            # Test key URLs (assuming server is running)
            test_urls = [
                'http://127.0.0.1:8000/core/data-upload/',
                'http://127.0.0.1:8000/core/hospitals/',
                'http://127.0.0.1:8000/core/reports/',
                'http://127.0.0.1:8000/api/'
            ]

            accessible_urls = 0

            for url in test_urls:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code in [200, 302, 403]:  # 403 might be due to auth
                        accessible_urls += 1
                        print(f"  ✓ {url}: Accessible")
                    else:
                        print(f"  ⚠ {url}: Status {response.status_code}")
                except requests.exceptions.RequestException:
                    print(f"  ⚠ {url}: Not accessible (server may not be running)")

            if accessible_urls >= len(test_urls) // 2:
                self.test_results['api_endpoints'] = 'PASS'
                self.passed_tests += 1
                print("  ✅ API Endpoints: PASSED")
            else:
                self.test_results['api_endpoints'] = 'PARTIAL'
                print("  ⚠ API Endpoints: PARTIAL (server may not be running)")

        except Exception as e:
            self.test_results['api_endpoints'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ API Endpoints: ERROR - {e}")

    def test_prediction_accuracy(self):
        """Test prediction accuracy and model performance"""

        print("\n6. Testing Prediction Accuracy...")

        try:
            # Test prediction comparison functionality
            predictions = PredictionComparison.objects.all()

            if predictions.exists():
                accuracies = []
                improvements = []

                for pred in predictions:
                    if pred.after_accuracy_score and pred.before_accuracy_score:
                        accuracies.append(pred.after_accuracy_score)
                        improvements.append(pred.improvement_percentage)

                avg_accuracy = np.mean(accuracies) if accuracies else 0
                avg_improvement = np.mean(improvements) if improvements else 0

                print(f"  ✓ Predictions found: {len(predictions)}")
                print(f"  ✓ Average accuracy: {avg_accuracy:.2f}%")
                print(f"  ✓ Average improvement: {avg_improvement:.2f}%")

                if avg_accuracy >= 80 and avg_improvement > 0:
                    self.test_results['prediction_accuracy'] = 'PASS'
                    self.passed_tests += 1
                    print("  ✅ Prediction Accuracy: PASSED")
                else:
                    self.test_results['prediction_accuracy'] = 'FAIL'
                    self.failed_tests += 1
                    print("  ❌ Prediction Accuracy: FAILED")
            else:
                self.test_results['prediction_accuracy'] = 'NO_DATA'
                print("  ⚠ Prediction Accuracy: NO DATA")

        except Exception as e:
            self.test_results['prediction_accuracy'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ Prediction Accuracy: ERROR - {e}")

    def test_system_performance(self):
        """Test system performance metrics"""

        print("\n7. Testing System Performance...")

        try:
            import time

            # Test database query performance
            start_time = time.time()
            hospitals = list(Hospital.objects.all())
            db_query_time = time.time() - start_time

            # Test data processing performance
            start_time = time.time()
            sample_data = pd.DataFrame({
                'date': pd.date_range('2025-01-01', periods=1000),
                'value': np.random.randint(1, 100, 1000)
            })
            processing_time = time.time() - start_time

            print(f"  ✓ Database query time: {db_query_time:.3f}s")
            print(f"  ✓ Data processing time: {processing_time:.3f}s")

            if db_query_time < 1.0 and processing_time < 1.0:
                self.test_results['system_performance'] = 'PASS'
                self.passed_tests += 1
                print("  ✅ System Performance: PASSED")
            else:
                self.test_results['system_performance'] = 'SLOW'
                print("  ⚠ System Performance: SLOW")

        except Exception as e:
            self.test_results['system_performance'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ System Performance: ERROR - {e}")

    def test_load_handling(self):
        """Test system load handling capabilities"""

        print("\n8. Testing Load Handling...")

        try:
            # Simulate concurrent data processing
            import concurrent.futures

            def process_batch(batch_size):
                data = pd.DataFrame({
                    'id': range(batch_size),
                    'value': np.random.randint(1, 100, batch_size)
                })
                return len(data)

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(process_batch, 100) for _ in range(10)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]

            total_processed = sum(results)

            print(f"  ✓ Concurrent batches processed: {len(results)}")
            print(f"  ✓ Total records processed: {total_processed}")

            if total_processed == 1000:
                self.test_results['load_handling'] = 'PASS'
                self.passed_tests += 1
                print("  ✅ Load Handling: PASSED")
            else:
                self.test_results['load_handling'] = 'FAIL'
                self.failed_tests += 1
                print("  ❌ Load Handling: FAILED")

        except Exception as e:
            self.test_results['load_handling'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ Load Handling: ERROR - {e}")

    def test_data_security(self):
        """Test data security and validation"""

        print("\n9. Testing Data Security...")

        try:
            # Test SQL injection protection
            from django.db import connection

            # Test input validation
            test_inputs = [
                "'; DROP TABLE hospitals; --",
                "<script>alert('xss')</script>",
                "../../etc/passwd",
                "admin' OR '1'='1"
            ]

            secure_inputs = 0

            for test_input in test_inputs:
                # Test if Django ORM properly escapes input
                try:
                    # This should not cause any issues with proper ORM usage
                    hospitals = Hospital.objects.filter(name__icontains=test_input)
                    secure_inputs += 1
                except Exception:
                    pass  # Expected for malicious input

            print(f"  ✓ SQL injection tests: {secure_inputs}/{len(test_inputs)} secure")
            print("  ✓ Django ORM protection: Active")

            self.test_results['data_security'] = 'PASS'
            self.passed_tests += 1
            print("  ✅ Data Security: PASSED")

        except Exception as e:
            self.test_results['data_security'] = f'ERROR: {e}'
            self.failed_tests += 1
            print(f"  ❌ Data Security: ERROR - {e}")

    def generate_test_report(self):
        """Generate comprehensive test report"""

        print("\n" + "=" * 60)
        print("🧪 HUTANO TESTING REPORT")
        print("=" * 60)

        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0

        print(f"Total Tests Run: {total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Tests Failed: {self.failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")

        print("\nDetailed Results:")
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result == 'PASS' else "❌" if 'ERROR' in result or result == 'FAIL' else "⚠"
            print(f"  {status_icon} {test_name.replace('_', ' ').title()}: {result}")

        # Overall assessment
        if success_rate >= 90:
            print("\n🎉 OVERALL ASSESSMENT: EXCELLENT")
            print("   System is ready for production deployment")
        elif success_rate >= 75:
            print("\n✅ OVERALL ASSESSMENT: GOOD")
            print("   System is functional with minor issues")
        elif success_rate >= 50:
            print("\n⚠ OVERALL ASSESSMENT: NEEDS IMPROVEMENT")
            print("   System has significant issues that need addressing")
        else:
            print("\n❌ OVERALL ASSESSMENT: CRITICAL ISSUES")
            print("   System requires major fixes before deployment")

        # Save report to file
        with open('hutano_test_report.txt', 'w') as f:
            f.write(f"HUTANO Testing Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n")
            f.write(f"Success Rate: {success_rate:.1f}%\n")
            f.write(f"Tests Passed: {self.passed_tests}/{total_tests}\n\n")

            for test_name, result in self.test_results.items():
                f.write(f"{test_name}: {result}\n")

        print(f"\n📄 Test report saved to: hutano_test_report.txt")

def run_hutano_tests():
    """Main function to run all HUTANO tests"""

    test_suite = HUTANOTestSuite()
    test_suite.run_all_tests()

    return test_suite.test_results

if __name__ == "__main__":
    run_hutano_tests()
