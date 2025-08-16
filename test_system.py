#!/usr/bin/env python3
"""
Test script for Financial Portfolio Analysis System
Run this to verify all components are working correctly
"""

import requests
import json
import time
from typing import Dict, Any

class SystemTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    def test_health(self) -> bool:
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_agent_status(self) -> bool:
        """Test agent status endpoint"""
        try:
            response = requests.get(f"{self.base_url}/agents/status")
            if response.status_code == 200:
                data = response.json()
                print("✅ Agent status check passed")
                print(f"   Agents: {len(data['agents'])}")
                return True
            else:
                print(f"❌ Agent status failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Agent status error: {e}")
            return False
    
    def test_chat(self, message: str, language: str = "normal") -> bool:
        """Test chat endpoint"""
        try:
            payload = {
                "message": message,
                "language": language,
                "session_id": self.session_id
            }
            
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.session_id = data.get("session_id")
                print(f"✅ Chat test passed: {message[:50]}...")
                print(f"   Response length: {len(data['response'])} characters")
                return True
            else:
                print(f"❌ Chat test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Chat test error: {e}")
            return False
    
    def test_portfolio(self) -> bool:
        """Test portfolio endpoint"""
        try:
            response = requests.get(f"{self.base_url}/portfolio")
            if response.status_code == 200:
                data = response.json()
                print("✅ Portfolio test passed")
                print(f"   Total value: ₹{data['summary']['total_value']:,.0f}")
                return True
            else:
                print(f"❌ Portfolio test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Portfolio test error: {e}")
            return False
    
    def test_penny_stocks(self) -> bool:
        """Test penny stocks endpoint"""
        try:
            response = requests.get(f"{self.base_url}/portfolio/penny-stocks")
            if response.status_code == 200:
                data = response.json()
                print("✅ Penny stocks test passed")
                print(f"   Count: {data['count']} penny stocks")
                return True
            else:
                print(f"❌ Penny stocks test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Penny stocks test error: {e}")
            return False
    
    def test_examples(self) -> bool:
        """Test examples endpoint"""
        try:
            response = requests.get(f"{self.base_url}/examples")
            if response.status_code == 200:
                data = response.json()
                print("✅ Examples test passed")
                print(f"   Query categories: {len(data)}")
                return True
            else:
                print(f"❌ Examples test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Examples test error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive System Test")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health),
            ("Agent Status", self.test_agent_status),
            ("Portfolio Data", self.test_portfolio),
            ("Penny Stocks", self.test_penny_stocks),
            ("Examples", self.test_examples),
            ("Personal Query (Normal)", lambda: self.test_chat("Who is Ganesh Divekar?", "normal")),
            ("Portfolio Summary (GenZ)", lambda: self.test_chat("Show me my portfolio summary", "genz")),
            ("Penny Stocks Query", lambda: self.test_chat("What are my penny stocks?", "normal")),
            ("Investment Advice", lambda: self.test_chat("What should I buy?", "genz")),
            ("News Impact", lambda: self.test_chat("How does traffic issues in India affect my stocks?", "normal")),
            ("Performance Analysis", lambda: self.test_chat("Analyze my portfolio performance", "genz")),
            ("Risk Assessment", lambda: self.test_chat("Analyze my portfolio risk", "normal")),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            try:
                if test_func():
                    passed += 1
                time.sleep(1)  # Small delay between tests
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! System is ready for demo.")
        else:
            print("⚠️  Some tests failed. Please check the system configuration.")
        
        return passed == total

def main():
    """Main test function"""
    print("Financial Portfolio Analysis System - Test Suite")
    print("=" * 60)
    
    # Check if server is running
    tester = SystemTester()
    
    try:
        # Test if server is accessible
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not running. Please start the server first:")
            print("   python main.py")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python main.py")
        return False
    
    # Run comprehensive test
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎯 Demo Ready! You can now:")
        print("1. Open http://localhost:8000/docs for API documentation")
        print("2. Use the demo script for your presentation")
        print("3. Test different queries and language styles")
    
    return success

if __name__ == "__main__":
    main()
