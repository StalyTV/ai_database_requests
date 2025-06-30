#!/usr/bin/env python3
"""
Test script for natural language to SQL functionality
Demonstrates automated testing of the natural language interface
"""

from API import ConstructionProjectAPI
import json

def test_natural_language_queries():
    """Test various natural language queries."""
    
    api = ConstructionProjectAPI()
    
    # Test queries
    test_queries = [
        "Show all elements in the ground floor",
        "How many smoke detectors are needed in total?",
        "List all electrical elements",
        "What fire safety elements are in the basement?"
    ]
    
    print("=== Testing Natural Language to SQL Conversion ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. Testing: '{query}'")
        print("-" * 60)
        
        try:
            result = api.query_from_natural_language(query)
            
            if result['success']:
                print(f"✓ SQL Generated: {result['sql_query']}")
                print(f"✓ Natural Language Response:")
                print(f"  {result['natural_response']}")
                print(f"✓ Raw Data: {len(result['results'])} rows returned")
                
                # Show first few results for reference
                if result['results'] and len(result['results']) <= 5:
                    print("Raw results:")
                    for j, row in enumerate(result['results']):
                        print(f"  Row {j+1}: {dict(row)}")
                    
            else:
                print(f"✗ Error: {result['error']}")
                print(f"Natural Language Response: {result['natural_response']}")
                
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_natural_language_queries()
