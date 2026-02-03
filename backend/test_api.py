#!/usr/bin/env python3

import requests
import json
import time

def test_api():
    base_url = "http://localhost:5000/api"
    
    print("Testing EVPulse API...")
    print("="*50)
    
    # Test endpoints
    endpoints = [
        "/health",
        "/stations",
        "/auth/login"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\nTesting {endpoint}...")
            url = f"{base_url}{endpoint}"
            
            if endpoint == "/auth/login":
                # Test login with mock data
                response = requests.post(url, json={
                    "email": "user@evpulse.com",
                    "password": "user123"
                }, timeout=10)
            else:
                response = requests.get(url, timeout=10)
                
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed to {endpoint}")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout connecting to {endpoint}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Wait a moment for server to be ready
    time.sleep(2)
    test_api()