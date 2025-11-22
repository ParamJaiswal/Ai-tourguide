"""
Quick demo showing the enhanced tourist guide in action.
Run this with the server active to see real responses.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_query(query, description):
    """Test a query and show the response."""
    print(f"\n{'='*80}")
    print(f"📝 {description}")
    print(f"   Query: \"{query}\"")
    print(f"{'='*80}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/tourism/query",
            json={"query": query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"\n{data.get('message', 'No message')}\n")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ Server not running! Start it with: python -m app.main")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    print("\n" + "="*80)
    print("🧳 ENHANCED TOURIST GUIDE - LIVE DEMO")
    print("="*80)
    print("\nMake sure the server is running: python -m app.main")
    print("Then this script will show you the enhanced responses!\n")
    
    # Test queries showcasing the improvements
    test_cases = [
        ("Bangalore", "🎯 Just city name - Auto tourist guide mode"),
        ("Parris", "✏️ Typo correction + Auto guide mode"),
        ("Weather in London", "🌤️ Weather with personality"),
        ("Tokyo", "🗾 Minimal query - Shows exciting places"),
        ("Tell me about Dubai", "💬 Conversational query"),
    ]
    
    for query, description in test_cases:
        test_query(query, description)
        input("\n👉 Press Enter for next example...")
    
    print("\n" + "="*80)
    print("✨ Demo Complete!")
    print("="*80)
    print("\nKey Improvements You Saw:")
    print("  ✅ Auto-shows places when you just type a city name")
    print("  ✅ Friendly, emoji-rich responses")
    print("  ✅ Weather with clothing recommendations")
    print("  ✅ Helpful tips and suggestions")
    print("  ✅ Spell correction that works seamlessly")
    print("\nThe system now truly acts as your personal tour guide! 🧳✨\n")

if __name__ == "__main__":
    main()
