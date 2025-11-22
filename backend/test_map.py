"""Test script for map generation functionality."""

import asyncio
from app.services.places import get_tourist_attractions
from app.services.map_service import create_enhanced_map_html
from app.services.geocoding import get_coordinates

async def test_map_generation():
    """Test map generation for a city."""
    
    print("🗺️  Testing Map Generation Feature\n")
    print("="*60)
    
    # Test cities
    test_cities = [
        "Paris",
        "Tokyo",
        "New York",
        "Bangalore"
    ]
    
    for city in test_cities:
        print(f"\n📍 Testing: {city}")
        print("-"*60)
        
        try:
            # Get coordinates
            coords = await get_coordinates(city)
            lat, lon = coords['lat'], coords['lon']
            print(f"✓ Coordinates: {lat}, {lon}")
            
            # Get tourist attractions
            places = await get_tourist_attractions(lat, lon)
            print(f"✓ Found {len(places)} places")
            
            if places:
                print("\n  Places:")
                for idx, place in enumerate(places, 1):
                    print(f"    {idx}. {place['name']} ({place['type']})")
                
                # Generate map
                map_html = create_enhanced_map_html(
                    city_name=city,
                    city_lat=lat,
                    city_lon=lon,
                    places=places,
                    weather_info={"temp": 25.0, "precipitation": 30}  # Sample data
                )
                
                # Save map to file
                filename = f"map_{city.lower().replace(' ', '_')}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(map_html)
                
                print(f"\n✓ Map saved to: {filename}")
                print(f"  Open this file in your browser to view the interactive map!")
            else:
                print("  ⚠️ No places found for this city")
        
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    print("\n" + "="*60)
    print("✅ Map generation test complete!")
    print("\nGenerated map files can be opened in any web browser.")
    print("They include:")
    print("  • Interactive markers for each attraction")
    print("  • Sidebar with attraction list and weather")
    print("  • Fullscreen and measurement tools")
    print("  • Beautiful gradient design")

if __name__ == "__main__":
    asyncio.run(test_map_generation())
