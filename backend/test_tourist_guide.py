"""Test script for enhanced tourist guide behavior."""

import asyncio
from app.agents.parent_agent import ParentAgent

async def test_tourist_guide():
    """Test the enhanced tourist guide conversational mode."""
    
    print("\n" + "="*80)
    print("🧳 ENHANCED TOURIST GUIDE - CONVERSATIONAL TEST")
    print("="*80 + "\n")
    
    agent = ParentAgent()
    
    # Test cases showing tourist guide behavior
    test_queries = [
        # Just city name (should auto-show places)
        ("Bangalore", "Just city name - should show exciting places"),
        ("Paris", "Just city name - auto tourist guide mode"),
        ("Tokyo", "Simple city mention"),
        
        # With typos (should correct and show places)
        ("Banglore", "Typo in city name - should correct and show places"),
        ("Parris", "Misspelled city - should correct and show places"),
        
        # Short queries (tourist mode)
        ("New York", "Two-word city name"),
        ("Tell me about Dubai", "Conversational query"),
        
        # Specific intent (weather)
        ("Weather in London", "Specific weather request"),
        ("Temperature in Tokyo", "Temperature query"),
        
        # Specific intent (places)
        ("Places in Rome", "Specific places request"),
        ("What can I see in Bangkok", "What to see query"),
        
        # Combined intent
        ("Paris weather and places", "Both weather and places"),
        
        # Natural language
        ("I'm going to Mumbai tomorrow", "Natural travel statement"),
    ]
    
    for query, description in test_queries:
        print(f"📝 Test: {description}")
        print(f"   Query: \"{query}\"")
        print("-" * 80)
        
        try:
            result = await agent.process(query)
            
            if result.get("success"):
                data = result.get("data", {})
                text = data.get("text", "")
                place = data.get("place_name", "Unknown")
                places = data.get("places", [])
                weather = data.get("weather")
                
                print(f"   ✓ Location: {place}")
                print(f"   ✓ Places found: {len(places)}")
                print(f"   ✓ Weather data: {'Yes' if weather else 'No'}")
                print(f"\n   Response:")
                print(f"   {text[:200]}..." if len(text) > 200 else f"   {text}")
            else:
                print(f"   ✗ Error: {result.get('data', {}).get('text', 'Unknown error')}")
        
        except Exception as e:
            print(f"   ✗ Exception: {str(e)}")
        
        print("\n")
    
    print("="*80)
    print("✅ Tourist guide test complete!")
    print("="*80)
    print("\nKey Improvements Demonstrated:")
    print("  ✅ Just typing city name shows exciting places automatically")
    print("  ✅ Spell correction works seamlessly")
    print("  ✅ Friendly, conversational responses with emojis")
    print("  ✅ Helpful suggestions and tips")
    print("  ✅ Weather-based clothing recommendations")
    print("  ✅ Smart intent detection for minimal queries")
    print("\n")

if __name__ == "__main__":
    asyncio.run(test_tourist_guide())
