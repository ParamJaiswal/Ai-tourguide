"""Test script for the enhanced text parser."""

from app.utils.text_parser import EnhancedTextParser

def test_parser():
    parser = EnhancedTextParser()
    
    test_cases = [
        # Spell correction tests
        ("What's the weather in Banglore?", "Bangalore", True),
        ("I'm going to Parris", "Paris", True),
        ("Places to visit in NYC", "New York", True),
        ("Temperature in LA", "Los Angeles", True),
        
        # Natural language tests
        ("I'm heading to Tokyo tomorrow", "Tokyo", False),
        ("What can I see in London?", "London", False),
        ("Tell me about Dubai weather and attractions", "Dubai", False),
        
        # Multi-word cities
        ("Weather in New York City", "New York", False),
        ("Going to San Francisco", "San Francisco", False),
        
        # Intent detection tests
        ("What's the temperature in Paris?", "Paris", False),  # weather only
        ("Places to visit in Rome", "Rome", False),  # places only
        ("I'm visiting Tokyo, what's the weather and what can I see?", "Tokyo", False),  # both
    ]
    
    print("\n" + "="*80)
    print("ENHANCED TEXT PARSER TEST RESULTS")
    print("="*80 + "\n")
    
    passed = 0
    failed = 0
    
    for query, expected_location, should_correct in test_cases:
        result = parser.parse_query(query)
        location = result['location']
        was_corrected = result['was_corrected']
        intent = result['intent']
        
        # Check if location matches
        location_match = location == expected_location
        
        # Check if correction happened as expected
        correction_match = was_corrected == should_correct
        
        # Overall success
        success = location_match and correction_match
        
        if success:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status}")
        print(f"  Query: {query}")
        print(f"  Expected: {expected_location} (corrected: {should_correct})")
        print(f"  Got: {location} (corrected: {was_corrected})")
        print(f"  Intent: Weather={intent['weather']}, Places={intent['places']}")
        print()
    
    print("="*80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("="*80)
    
    return passed, failed

if __name__ == "__main__":
    passed, failed = test_parser()
    exit(0 if failed == 0 else 1)
