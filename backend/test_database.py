#!/usr/bin/env python3
"""
Test script to verify database functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_qr_generation():
    """Test QR code generation with database storage"""
    print("Testing QR code generation...")
    
    # Test data
    qr_data = {
        "content": "https://example.com",
        "qr_type": "url",
        "title": "Test QR Code",
        "description": "A test QR code for database verification",
        "size": 10,
        "foreground_color": "#000000",
        "background_color": "#FFFFFF"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/qr/generate", json=qr_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"QR ID: {result.get('qr_id')}")
        print(f"Success: {result.get('success')}")
        return result.get('qr_id')
    else:
        print(f"Error: {response.text}")
        return None

def test_get_designs():
    """Test getting all designs"""
    print("Testing get all designs...")
    response = requests.get(f"{BASE_URL}/api/v1/qr/designs")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        designs = response.json()
        print(f"Found {len(designs)} designs")
        for design in designs:
            print(f"  - {design.get('title', 'No title')} (ID: {design.get('id')})")
    else:
        print(f"Error: {response.text}")
    print()

def test_get_design(design_id):
    """Test getting a specific design"""
    if not design_id:
        return
    
    print(f"Testing get design {design_id}...")
    response = requests.get(f"{BASE_URL}/api/v1/qr/designs/{design_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        design = response.json()
        print(f"Title: {design.get('title')}")
        print(f"Content: {design.get('content')}")
        print(f"Type: {design.get('qr_type')}")
    else:
        print(f"Error: {response.text}")
    print()

def test_search_designs():
    """Test searching designs"""
    print("Testing search designs...")
    response = requests.get(f"{BASE_URL}/api/v1/qr/designs/search/test")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        results = response.json()
        print(f"Found {len(results)} matching designs")
    else:
        print(f"Error: {response.text}")
    print()

def main():
    """Run all tests"""
    print("🚀 QuickQR Database Test Suite")
    print("=" * 40)
    
    # Test health
    test_health()
    
    # Test QR generation
    design_id = test_qr_generation()
    
    # Test getting all designs
    test_get_designs()
    
    # Test getting specific design
    test_get_design(design_id)
    
    # Test search
    test_search_designs()
    
    print("✅ Database test completed!")

if __name__ == "__main__":
    main() 