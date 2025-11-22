# 🗺️ Interactive Map Feature Documentation

## Overview

The tourism system now includes **interactive map visualization** that shows tourist attractions marked on a beautiful, interactive map! This feature provides a visual way to explore cities and their famous spots.

## Features

### ✨ What's Included

1. **Interactive Map**
   - Pan and zoom capabilities
   - Click markers for detailed information
   - Fullscreen mode
   - Distance measurement tool

2. **Visual Elements**
   - 🏠 Red marker for city center
   - ⭐ Color-coded markers for different attraction types:
     - 🟣 Purple: Museums
     - 🔵 Blue: General attractions
     - 🟢 Green: Parks
     - 🔴 Dark Blue: Monuments
     - 🟠 Orange: Viewpoints
   
3. **Information Sidebar**
   - City name and statistics
   - Current weather (if requested)
   - List of top attractions
   - Helpful tips

4. **Map Features**
   - Search radius visualization (10km circle)
   - Lines connecting city center to attractions
   - Detailed popups for each location
   - Legend explaining markers
   - Responsive design (works on mobile!)

## How to Use

### Method 1: API Endpoint

```bash
# Request a map for a city
curl -X POST http://localhost:8000/api/tourism/map \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me Paris"}'
```

This returns an HTML page that you can open in your browser.

### Method 2: Save to File

```bash
# Save map to a file
curl -X POST http://localhost:8000/api/tourism/map \
  -H "Content-Type: application/json" \
  -d '{"query": "Map of Tokyo"}' \
  > tokyo_map.html

# Then open tokyo_map.html in your browser
```

### Method 3: Direct Browser Access

1. Start the server:
   ```bash
   python -m app.main
   ```

2. Use Swagger UI at http://localhost:8000/docs

3. Try the `/api/tourism/map` endpoint with queries like:
   - "Show me Paris"
   - "Map of Tokyo"
   - "Places in New York"
   - "Attractions in Bangalore"

## Query Examples

### Simple Queries
```
"Show me Paris"
"Map of London"
"Tokyo map"
```

### With Places
```
"Show attractions in Rome"
"Map of Barcelona with places"
"Where to visit in Sydney"
```

### With Weather
```
"Paris map with weather"
"Show me Tokyo with temperature"
```

### Natural Language
```
"I want to see a map of New York"
"Can you show me places in Dubai?"
"Map view of Singapore please"
```

## What You'll See

### Map Elements

1. **City Center Marker (Red Home Icon)**
   - Shows the main coordinates of the city
   - Popup includes city name and weather (if available)

2. **Attraction Markers (Colored Stars/Icons)**
   - Each tourist attraction gets a marker
   - Color indicates type (museum, park, monument, etc.)
   - Numbered 1-5 based on discovery order
   - Click for detailed information

3. **Connection Lines**
   - Dotted gray lines from city center to each attraction
   - Helps visualize distances

4. **Search Radius Circle**
   - Light blue circle showing 10km search area
   - Helps understand coverage

### Sidebar Information

**Top Section:**
- City name
- Number of places found
- Search radius

**Weather Section** (if weather was requested):
- Current temperature
- Rain chance percentage

**Attractions List:**
- Numbered list of all places
- Attraction type for each
- Matches the markers on the map

## Map Controls

### Built-in Controls

1. **Zoom Buttons**
   - `+` to zoom in
   - `-` to zoom out
   - Or use mouse wheel

2. **Fullscreen Button**
   - Top-right corner
   - Expands map to full screen
   - Press ESC to exit

3. **Measure Tool**
   - Click to start measuring
   - Click multiple points
   - Shows distance in km and miles

4. **Pan**
   - Click and drag to move around
   - Touch gestures on mobile

## Technical Details

### API Response

The `/api/tourism/map` endpoint returns:
- **Content-Type**: `text/html`
- **Status Code**: 200 (success) or 400/500 (error)

### Map Generation

Uses **Folium** (Python wrapper for Leaflet.js):
- Industry-standard mapping library
- Renders OpenStreetMap tiles
- Fully interactive and responsive
- No API keys required!

### Data Sources

1. **City Coordinates**: Nominatim OpenStreetMap API
2. **Tourist Attractions**: Overpass API (OpenStreetMap)
3. **Weather Data**: Open-Meteo API (if requested)
4. **Map Tiles**: OpenStreetMap

## Customization Options

### In the Code

You can customize in `map_service.py`:

```python
# Change search radius
create_city_map(radius=15000)  # 15km instead of 10km

# Change colors
type_colors = {
    'museum': 'purple',  # Change to your preferred color
    'park': 'green',
    # ...
}

# Change zoom level
m = folium.Map(zoom_start=13)  # Closer zoom
```

## Example Use Cases

### 1. Trip Planning
```
Query: "Map of Paris"
Use: See all attractions before visiting
Action: Click markers to learn about each place
```

### 2. Quick Overview
```
Query: "Show me Tokyo with weather"
Use: Get visual layout + weather in one view
Action: Plan based on weather and distances
```

### 3. Distance Estimation
```
Query: "Map of New York"
Use: See how far attractions are from center
Action: Use measure tool to plan walking routes
```

### 4. Local Exploration
```
Query: "Attractions in Bangalore"
Use: Find nearby places to visit
Action: Check which are clustered together
```

## Browser Compatibility

✅ **Fully Supported:**
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

✅ **Mobile:**
- iOS Safari
- Android Chrome
- Works on tablets

## Screenshots Description

### Desktop View
- Sidebar on left (350px width)
- Map takes remaining space
- Gradient purple background on sidebar
- Clean, modern design

### Mobile View
- Sidebar on top (40% height)
- Map below (60% height)
- Fully scrollable
- Touch-friendly controls

## Performance

- **Map Load Time**: ~1-2 seconds
- **File Size**: ~100-150 KB per map
- **Offline Capable**: Once loaded, basic interactions work offline
- **Caching**: Map tiles are cached by browser

## Troubleshooting

### Map Not Loading?
1. Check internet connection (needs to load map tiles)
2. Ensure JavaScript is enabled
3. Try a different browser
4. Check browser console for errors

### No Places Shown?
1. Try a major city (e.g., Paris, Tokyo, London)
2. Smaller towns may not have tourist data
3. Check the response - might say "No places found"

### Map Too Slow?
1. Close other browser tabs
2. Reduce zoom level
3. Try on a different device

## Code Examples

### Python - Generate Map Programmatically

```python
from app.services.map_service import create_enhanced_map_html
from app.services.places import get_tourist_attractions
from app.services.geocoding import get_coordinates

async def generate_map(city_name):
    # Get coordinates
    coords = await get_coordinates(city_name)
    
    # Get attractions
    places = await get_tourist_attractions(
        coords['lat'], 
        coords['lon']
    )
    
    # Generate map HTML
    map_html = create_enhanced_map_html(
        city_name=city_name,
        city_lat=coords['lat'],
        city_lon=coords['lon'],
        places=places,
        weather_info={"temp": 25, "precipitation": 20}
    )
    
    # Save to file
    with open(f"{city_name}_map.html", 'w') as f:
        f.write(map_html)
```

### JavaScript - Embed in Website

```javascript
// Fetch map from API
async function loadCityMap(cityQuery) {
    const response = await fetch('http://localhost:8000/api/tourism/map', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: cityQuery
        })
    });
    
    const mapHtml = await response.text();
    
    // Display in iframe
    const iframe = document.getElementById('map-frame');
    iframe.srcdoc = mapHtml;
}

// Usage
loadCityMap("Show me Paris");
```

## Future Enhancements

Potential additions (suggestions):

1. **Custom Markers**
   - User-defined points of interest
   - Photos on markers

2. **Route Planning**
   - Optimized route through all attractions
   - Walking/driving directions

3. **Filtering**
   - Filter by attraction type
   - Hide/show specific markers

4. **Export Options**
   - Download as PDF
   - Share link
   - Save favorite maps

5. **Real-time Updates**
   - Live crowd information
   - Opening hours
   - User ratings

## Support

For issues or questions:
1. Check this documentation
2. Review `map_service.py` code
3. Test with `test_map.py`
4. Check server logs

## Summary

The interactive map feature adds a powerful visual dimension to the tourism system. Instead of just text, users can now:
- **See** where attractions are located
- **Explore** cities visually
- **Plan** trips with distance information
- **Understand** spatial relationships

It's fully integrated, uses free APIs, and provides a modern, beautiful user experience!

---

**Happy Mapping! 🗺️✨**
