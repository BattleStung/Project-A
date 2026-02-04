#!/usr/bin/env python3
"""
Test Suite for AI Customer Support Assistant
Run this to verify everything works before deploying
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name, func):
        """Run a single test"""
        print(f"\n🧪 Testing: {name}")
        try:
            func()
            print(f"✅ PASSED")
            self.passed += 1
            self.tests.append({'name': name, 'status': 'passed'})
        except AssertionError as e:
            print(f"❌ FAILED: {str(e)}")
            self.failed += 1
            self.tests.append({'name': name, 'status': 'failed', 'error': str(e)})
        except Exception as e:
            print(f"💥 ERROR: {str(e)}")
            self.failed += 1
            self.tests.append({'name': name, 'status': 'error', 'error': str(e)})
    
    def summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        
        if self.failed == 0:
            print("\n🎉 All tests passed! Ready for deployment.")
        else:
            print("\n⚠️  Some tests failed. Review errors above.")
        print("="*60)

def test_server_running():
    """Test if server is accessible"""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, "Server not responding"

def test_generate_reply_basic():
    """Test basic reply generation"""
    data = {
        "message": "I want a refund",
        "business_name": "Test Corp",
        "tone": "professional",
        "industry": "general business",
        "add_signature": True
    }
    
    response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
    result = response.json()
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert result['success'] == True, "Success flag not True"
    assert 'reply' in result, "No reply in response"
    assert len(result['reply']) > 0, "Empty reply"
    assert 'Test Corp' in result['reply'], "Business name not in signature"

def test_generate_reply_no_signature():
    """Test reply without signature"""
    data = {
        "message": "Hello, I need help",
        "business_name": "Test Corp",
        "tone": "friendly",
        "industry": "e-commerce",
        "add_signature": False
    }
    
    response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
    result = response.json()
    
    assert result['success'] == True
    assert 'Test Corp' not in result['reply'], "Signature present when disabled"

def test_input_validation_empty():
    """Test empty message validation"""
    data = {
        "message": "",
        "business_name": "Test Corp"
    }
    
    response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
    result = response.json()
    
    assert response.status_code == 400, "Should reject empty message"
    assert result['success'] == False, "Should not succeed with empty input"

def test_input_validation_unsafe():
    """Test unsafe content filtering"""
    data = {
        "message": "<script>alert('hack')</script>",
        "business_name": "Test Corp"
    }
    
    response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
    result = response.json()
    
    assert response.status_code == 400, "Should reject unsafe content"

def test_different_tones():
    """Test different tone settings"""
    tones = ['professional', 'friendly', 'casual', 'empathetic']
    
    for tone in tones:
        data = {
            "message": "I have a problem",
            "business_name": "Test",
            "tone": tone
        }
        
        response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
        result = response.json()
        
        assert result['success'] == True, f"Failed for tone: {tone}"
        assert result['metadata']['settings_used']['tone'] == tone

def test_different_industries():
    """Test different industry settings"""
    industries = ['general business', 'e-commerce', 'SaaS', 'healthcare']
    
    for industry in industries:
        data = {
            "message": "I need assistance",
            "business_name": "Test",
            "industry": industry
        }
        
        response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
        result = response.json()
        
        assert result['success'] == True, f"Failed for industry: {industry}"

def test_feedback_endpoint():
    """Test feedback submission"""
    data = {
        "customer_message": "Test message",
        "original_reply": "Original response",
        "edited_reply": "Edited response"
    }
    
    response = requests.post(f"{BASE_URL}/api/feedback", json=data)
    result = response.json()
    
    assert response.status_code == 200
    assert result['success'] == True

def test_stats_endpoint():
    """Test statistics endpoint"""
    response = requests.get(f"{BASE_URL}/api/stats")
    result = response.json()
    
    assert response.status_code == 200
    assert result['success'] == True
    assert 'stats' in result
    assert 'total_interactions' in result['stats']
    assert 'accuracy_rate' in result['stats']

def test_response_time():
    """Test that responses are reasonably fast"""
    data = {
        "message": "Quick test",
        "business_name": "Test"
    }
    
    start = time.time()
    response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 5, f"Response too slow: {duration:.2f}s"
    print(f"   Response time: {duration:.2f}s")

def test_concurrent_requests():
    """Test handling multiple requests"""
    import concurrent.futures
    
    def make_request():
        data = {
            "message": "Concurrent test",
            "business_name": "Test"
        }
        response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
        return response.status_code == 200
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    assert all(results), "Some concurrent requests failed"

def test_long_message_handling():
    """Test handling of very long messages"""
    long_message = "This is a test. " * 200  # ~3000 chars
    
    data = {
        "message": long_message,
        "business_name": "Test"
    }
    
    response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
    result = response.json()
    
    assert response.status_code == 200
    assert result['success'] == True
    # Message should be truncated
    assert len(result['metadata']['cleaned_message']) <= 2003  # 2000 + "..."

def test_special_characters():
    """Test handling of special characters"""
    data = {
        "message": "Hello! I need help with émojis 😊 and spëcial çharacters",
        "business_name": "Test"
    }
    
    response = requests.post(f"{BASE_URL}/api/generate-reply", json=data)
    result = response.json()
    
    assert response.status_code == 200
    assert result['success'] == True

def main():
    print("="*60)
    print("🧪 AI CUSTOMER SUPPORT ASSISTANT - TEST SUITE")
    print("="*60)
    print(f"Testing server at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    runner = TestRunner()
    
    # Connection tests
    runner.test("Server is running", test_server_running)
    
    # Functionality tests
    runner.test("Generate basic reply", test_generate_reply_basic)
    runner.test("Generate reply without signature", test_generate_reply_no_signature)
    
    # Validation tests
    runner.test("Reject empty message", test_input_validation_empty)
    runner.test("Reject unsafe content", test_input_validation_unsafe)
    
    # Configuration tests
    runner.test("Different tones work", test_different_tones)
    runner.test("Different industries work", test_different_industries)
    
    # API endpoint tests
    runner.test("Feedback endpoint works", test_feedback_endpoint)
    runner.test("Stats endpoint works", test_stats_endpoint)
    
    # Performance tests
    runner.test("Response time acceptable", test_response_time)
    runner.test("Handle concurrent requests", test_concurrent_requests)
    
    # Edge case tests
    runner.test("Handle long messages", test_long_message_handling)
    runner.test("Handle special characters", test_special_characters)
    
    # Show summary
    runner.summary()
    
    # Save test results
    report = {
        'timestamp': datetime.now().isoformat(),
        'total': runner.passed + runner.failed,
        'passed': runner.passed,
        'failed': runner.failed,
        'tests': runner.tests
    }
    
    with open('test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n💾 Test report saved to: test_report.json")
    
    return runner.failed == 0

if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Make sure the server is running:")
        print("  python app.py")
        print(f"  at {BASE_URL}")
        exit(1)