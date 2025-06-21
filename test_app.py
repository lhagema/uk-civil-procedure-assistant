#!/usr/bin/env python3
"""
Simple test script for the Legal AI Assistant
"""

import requests
import json

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    # Test questions
    test_questions = [
        "When do witness statements need to be exchanged?",
        "How does the court allocate cases to a track?",
        "What are the time limits for serving particulars of claim?",
        "How do I make an application to strike out a statement of case?",
        "What is the weather like today?"  # This should return a fallback response
    ]
    
    print("🧪 Testing Legal AI Assistant API")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Testing: {question}")
        
        try:
            response = requests.post(
                f"{base_url}/api/query",
                data={"query": question},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result['success']}")
                print(f"   📝 Answer: {result['answer'][:100]}...")
                if result['citations']:
                    print(f"   📚 Citations: {', '.join(result['citations'])}")
                else:
                    print(f"   📚 Citations: None")
            else:
                print(f"   ❌ Error: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON decode error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")

if __name__ == "__main__":
    test_api() 