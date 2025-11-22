"""
Demo Script - Enhanced Tourism System
Shows the improvements in action with real examples
"""

from app.utils.text_parser import EnhancedTextParser

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def demo_query(parser, query, description):
    print(f"📝 {description}")
    print(f"   Query: \"{query}\"")
    
    result = parser.parse_query(query)
    
    print(f"   ✓ Location: {result['location']}")
    if result['was_corrected']:
        print(f"   ✓ Auto-corrected from typo!")
    if result['suggestions']:
        print(f"   💡 Suggestions: {', '.join(result['suggestions'])}")
    print(f"   ✓ Intent: ", end="")
    intents = []
    if result['intent']['weather']:
        intents.append("Weather")
    if result['intent']['places']:
        intents.append("Places")
    print(" + ".join(intents))
    print()

def main():
    print_header("🌟 ENHANCED TOURISM SYSTEM - LIVE DEMO 🌟")
    
    parser = EnhancedTextParser()
    
    # Demo 1: Spell Correction
    print_header("1️⃣  AUTOMATIC SPELL CORRECTION")
    demo_query(
        parser,
        "What's the weather in Banglore?",
        "Common misspelling of Bangalore"
    )
    demo_query(
        parser,
        "I'm going to Parris tomorrow",
        "Misspelled Paris"
    )
    demo_query(
        parser,
        "Temperature in Londan",
        "Typo in London"
    )
    
    # Demo 2: City Aliases
    print_header("2️⃣  CITY ALIAS RECOGNITION")
    demo_query(
        parser,
        "What can I see in NYC?",
        "NYC → New York"
    )
    demo_query(
        parser,
        "Weather in LA today",
        "LA → Los Angeles"
    )
    demo_query(
        parser,
        "Tell me about SF",
        "SF → San Francisco"
    )
    
    # Demo 3: Natural Language
    print_header("3️⃣  NATURAL LANGUAGE UNDERSTANDING")
    demo_query(
        parser,
        "I'm heading to Tokyo tomorrow, what should I pack?",
        "Conversational query with temporal context"
    )
    demo_query(
        parser,
        "Tell me about Dubai weather and attractions",
        "Combined request in natural language"
    )
    demo_query(
        parser,
        "Going to visit London next week",
        "Informal travel planning query"
    )
    
    # Demo 4: Multi-word Cities
    print_header("4️⃣  MULTI-WORD LOCATION SUPPORT")
    demo_query(
        parser,
        "Weather in New York City",
        "Three-word city name"
    )
    demo_query(
        parser,
        "Places to visit in San Francisco",
        "Two-word city name"
    )
    demo_query(
        parser,
        "How hot is Mexico City?",
        "Two-word city with question"
    )
    
    # Demo 5: Intent Detection
    print_header("5️⃣  SMART INTENT DETECTION")
    demo_query(
        parser,
        "What's the temperature in Paris?",
        "Weather-only query"
    )
    demo_query(
        parser,
        "Tourist attractions in Rome",
        "Places-only query"
    )
    demo_query(
        parser,
        "I'm visiting Tokyo, what's the weather and what can I see?",
        "Combined weather + places query"
    )
    
    # Demo 6: Complex Scenarios
    print_header("6️⃣  COMPLEX REAL-WORLD SCENARIOS")
    demo_query(
        parser,
        "Im going to Banglore tomorow, whats the wheather?",
        "Multiple typos + informal language"
    )
    demo_query(
        parser,
        "Heading to NYC next week, need weather and places info",
        "Alias + combined intent + conversational"
    )
    demo_query(
        parser,
        "Bombay weather",
        "Old city name (alias) + minimal query"
    )
    
    # Summary
    print_header("✨ DEMO COMPLETE ✨")
    print("Key Features Demonstrated:")
    print("  ✅ Automatic spell correction (80%+ similarity)")
    print("  ✅ City alias recognition (NYC, LA, SF, etc.)")
    print("  ✅ Natural language understanding")
    print("  ✅ Multi-word location support")
    print("  ✅ Smart intent detection")
    print("  ✅ Real-world scenario handling")
    print("\n" + "="*80)
    print("\n🚀 The tourism system is now tourist-friendly!")
    print("   Try your own queries with the API or test script.\n")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
