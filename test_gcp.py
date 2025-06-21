#!/usr/bin/env python3
"""
Test script to verify GCP integration
"""

import os
from gcp_integration import enhanced_legal_query, setup_gcp_environment

def test_gcp_integration():
    """Test the GCP integration"""
    print("🧪 Testing GCP Integration...")
    
    # Check environment
    if not setup_gcp_environment():
        print("❌ GCP environment not configured")
        return False
    
    # Test a simple query
    test_query = "What are the time limits for filing a defence?"
    print(f"📝 Testing query: {test_query}")
    
    try:
        result = enhanced_legal_query(test_query)
        print(f"✅ Query successful: {result['success']}")
        if result['success']:
            print(f"📄 Answer: {result['answer'][:200]}...")
        else:
            print(f"❌ Error: {result['answer']}")
        return result['success']
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    test_gcp_integration() 