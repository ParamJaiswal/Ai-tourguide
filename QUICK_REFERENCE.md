# 🚀 Quick Reference Card - Tourism System v2.0

## Start the Server
```bash
cd backend
python -m app.main
```
**Access:** http://localhost:8000/docs

---

## API Endpoints

### 1. Text Query (JSON Response)
```bash
POST /api/tourism/query
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Weather in NYC?"}'
```

### 2. Map View (HTML Response) 🗺️ NEW!
```bash
POST /api/tourism/map
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/tourism/map \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me Paris"}' > map.html
```

---

## Sample Queries

### Weather
```
"What's the weather in Bangalore?"
"Temperature in LA"           ← Recognizes alias
"How hot is Parris?"          ← Auto-corrects spelling
```

### Places
```
"What can I see in Tokyo?"
"Places to visit in NYC"      ← Recognizes alias
"Attractions in Londan"       ← Auto-corrects spelling
```

### Combined
```
"I'm visiting Paris, what's the weather and what can I see?"
"Tell me about Dubai"
```

### Maps 🗺️
```
"Show me Paris"
"Map of Tokyo"
"Places in New York"
"Attractions in Bangalore"
```

---

## Testing

### Test Text Parser
```bash
cd backend
python demo.py          # Interactive demo
python test_parser.py   # Run all tests
```

### Test Map Generation
```bash
cd backend
python test_map.py      # Generates 4 maps
```

### View Generated Maps
```bash
# After running test_map.py, open in browser:
map_paris.html
map_tokyo.html
map_new_york.html
map_bangalore.html
```

---

## Features at a Glance

| Feature | Description | Example |
|---------|-------------|---------|
| Spell Correction | Auto-fixes typos | "Banglore" → "Bangalore" |
| City Aliases | Recognizes abbreviations | "NYC" → "New York" |
| Natural Language | Understands conversation | "I'm going to..." |
| Interactive Maps | Visual attraction view | Colored markers on map |
| Weather Info | Current temperature | "25°C, 30% rain" |
| Place Coords | Exact locations | Lat/Lon for each place |

---

## Map Features

**Interactive Elements:**
- 🏠 Red: City center
- ⭐ Blue: Attractions
- 🏛️ Purple: Museums
- 🌳 Green: Parks
- 📏 Measure tool
- 🔍 Zoom controls
- 📱 Mobile friendly

---

## Response Examples

### Text Query Response
```json
{
  "success": true,
  "message": "In Paris it's 15°C with 20% rain...",
  "place_name": "Paris",
  "coordinates": {"lat": 48.85, "lon": 2.35}
}
```

### Map Query Response
```html
<!DOCTYPE html>
<html>
  <!-- Interactive map with attractions -->
  <!-- Sidebar with weather + list -->
  <!-- Fullscreen & measurement tools -->
</html>
```

---

## Documentation

| File | Purpose |
|------|---------|
| **README.md** | Main documentation |
| **MAP_FEATURE.md** | Complete map guide 🗺️ |
| **IMPROVEMENTS.md** | Text parser details |
| **QUICK_START.md** | Usage examples |
| **FEATURE_SUMMARY.md** | Complete overview |

---

## Common Issues & Solutions

### Map not loading?
✓ Check internet (needs map tiles)  
✓ Enable JavaScript  
✓ Try different browser

### No places found?
✓ Try major city (Paris, Tokyo)  
✓ Smaller towns have limited data  
✓ Check API response

### Server errors?
✓ Check requirements installed  
✓ Verify port 8000 available  
✓ Review server logs

---

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python -m app.main

# Test everything
python demo.py && python test_parser.py && python test_map.py

# Generate specific map
curl -X POST http://localhost:8000/api/tourism/map \
  -H "Content-Type: application/json" \
  -d '{"query": "Map of Paris"}' > paris.html && start paris.html

# Check health
curl http://localhost:8000/health
```

---

## Directory Quick Access

```
cd backend                           # Main code
cd backend/app/services              # Services (map, places, weather)
cd backend/app/utils                 # Text parser
cd backend/app/agents                # Agent logic
```

---

## Next Steps

1. ✅ Read **MAP_FEATURE.md** for map details
2. ✅ Run `test_map.py` to generate samples
3. ✅ Start server with `python -m app.main`
4. ✅ Try both endpoints in Swagger UI
5. ✅ Open generated maps in browser

---

## Pro Tips

💡 **For Best Results:**
- Use major cities for more attractions
- Request both weather and places for complete info
- Open maps in modern browsers (Chrome, Firefox)
- Use fullscreen mode for better viewing
- Try the measurement tool to check distances

💡 **For Development:**
- Check code comments in `map_service.py`
- Customize colors/icons in the service
- Add more cities to `text_parser.py`
- Extend with new features

---

## Support

🆘 **Need Help?**
1. Check relevant .md file
2. Run test scripts
3. Review code comments
4. Check server logs

📧 **Documentation:**
- MAP_FEATURE.md - Maps
- IMPROVEMENTS.md - Text parsing
- QUICK_START.md - General usage

---

**Version:** 2.0  
**Status:** Production Ready ✅  
**Last Updated:** November 2024

---

🎉 **Happy Tourism Exploring!** 🗺️✨
