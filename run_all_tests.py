#!/usr/bin/env python3
"""
Comprehensive Test Report Generator
"""
import subprocess
import json
import time
from datetime import datetime

def run_test(script_name, description):
    """Run a test script and capture results"""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=True,
            text=True,
            timeout=180
        )
        
        return {
            'name': description,
            'status': 'PASS' if result.returncode == 0 else 'FAIL',
            'returncode': result.returncode,
            'output': result.stdout
        }
    except subprocess.TimeoutExpired:
        return {
            'name': description,
            'status': 'TIMEOUT',
            'output': 'Test timed out after 180 seconds'
        }
    except Exception as e:
        return {
            'name': description,
            'status': 'ERROR',
            'output': str(e)
        }

print("=" * 70)
print("🚀 ARCGEN - COMPREHENSIVE TEST SUITE")
print("=" * 70)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Run all tests
tests = [
    ('test_e2e.py', 'End-to-End Diagram Generation Test'),
    ('test_features.py', 'API Features Test'),
    ('test_frontend.py', 'Frontend Integration Test'),
]

results = []
start_time = time.time()

for script, description in tests:
    result = run_test(script, description)
    results.append(result)
    print(result['output'])
    time.sleep(1)  # Small delay between tests

total_time = time.time() - start_time

# Generate summary
print("\n" + "=" * 70)
print("📊 FINAL TEST SUMMARY")
print("=" * 70)

passed = sum(1 for r in results if r['status'] == 'PASS')
failed = sum(1 for r in results if r['status'] in ['FAIL', 'ERROR'])
timeout = sum(1 for r in results if r['status'] == 'TIMEOUT')

print(f"\nTotal Tests: {len(results)}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"⏱️  Timeout: {timeout}")
print(f"⏰ Total Time: {total_time:.1f} seconds")

print("\nTest Results:")
for result in results:
    status_icon = {
        'PASS': '✅',
        'FAIL': '❌',
        'ERROR': '❌',
        'TIMEOUT': '⏱️'
    }.get(result['status'], '❓')
    
    print(f"  {status_icon} {result['name']}: {result['status']}")

if passed == len(results):
    print("\n" + "=" * 70)
    print("🎉 ALL TESTS PASSED! ARCGEN IS FULLY OPERATIONAL!")
    print("=" * 70)
    print("\n✅ System Status:")
    print("   ✓ Backend API: Working")
    print("   ✓ Frontend UI: Working")
    print("   ✓ AI Generation: Working")
    print("   ✓ CORS: Configured")
    print("   ✓ API Documentation: Available")
    print("\n🚀 Ready to use at: http://localhost:3000")
else:
    print(f"\n⚠️  {failed + timeout} test(s) failed or timed out")
    print("   Check the output above for details")

print("\n" + "=" * 70)
print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)
