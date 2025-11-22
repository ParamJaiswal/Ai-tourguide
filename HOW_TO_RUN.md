# 🚀 How to Run the Tourism System with Maps

## Quick Start (Step-by-Step)

### Step 1: Activate Virtual Environment
```bash
cd C:\Users\dell\.gemini\antigravity\scratch\inkle-tourism-system\backend
.\venv\Scripts\activate
```

### Step 2: Verify Folium is Installed
```bash
pip list | findstr folium
# Should show: folium   0.15.1
```

### Step 3: Start the Server
```bash
python -m app.main
```

**Server will start on:** http://localhost:8000

---

## Testing the Features

### Option 1: Use Swagger UI (Easiest!)
1. Open browser: http://localhost:8000/docs
2. Try the `/api/tourism/map` endpoint
3. Enter query: `"Show me Paris"`
4. Click "Execute"
5. Download the HTML response and open in browser

### Option 2: Use Command Line

**Generate a map:**
```powershell
# In a NEW terminal (keep server running)
cd C:\Users\dell\.gemini\antigravity\scratch\inkle-tourism-system\backend

# Generate Paris map
curl.exe -X POST http://localhost:8000/api/tourism/map `
  -H "Content-Type: application/json" `
  -d '{\"query\": \"Show me Paris\"}' `
  -o paris_map.html

# Open the map
start paris_map.html
```

**Get text response:**
```powershell
curl.exe -X POST http://localhost:8000/api/tourism/query `
  -H "Content-Type: application/json" `
  -d '{\"query\": \"Weather in NYC?\"}'
```

---

## Example Queries

### For Interactive Maps:
```
"Show me Paris"
"Map of Tokyo"
"Places in New York"
"Attractions in London"
"Bangalore map with weather"
```

### For Text Responses:
```
"What's the weather in Banglore?"  (auto-corrects to Bangalore)
"Places to visit in NYC"           (recognizes alias)
"I'm going to Paris tomorrow"      (natural language)
```

---

## Already Generated Maps

I've already created sample maps for you in the `backend` folder:
- ✅ `map_paris.html` - Paris attractions
- ✅ `map_tokyo.html` - Tokyo attractions
- ✅ `map_new_york.html` - New York attractions
- ✅ `map_bangalore.html` - Bangalore attractions
- ✅ `test_paris_map.html` - Latest test

**Just double-click any of these to open in your browser!**

---

## What You'll See in the Maps

### Map Features:
- 🗺️ Interactive OpenStreetMap
- 📍 Red marker for city center
- ⭐ Colored markers for attractions:
  - 🟣 Purple = Museums
  - 🔵 Blue = General attractions
  - 🟢 Green = Parks
  - 🔴 Dark Blue = Monuments

### Sidebar:
- City name
- Number of places found
- Weather info (if requested)
- List of top 5 attractions
- Tips and instructions

### Interactive Tools:
- 🔍 Zoom in/out
- 📏 Measure distances
- 📱 Fullscreen mode
- 👆 Click markers for details

---

## Troubleshooting

### Server won't start?
**Error: "ModuleNotFoundError: No module named 'folium'"**

Solution:
```bash
# Make sure venv is activated
.\venv\Scripts\activate

# Install folium in venv
pip install folium==0.15.1

# Try again
python -m app.main
```

### Map not loading?
- Check internet connection (needs to download map tiles)
- Try a different browser
- Check browser console for errors (F12)

### Port 8000 already in use?
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change port in main.py
```

---

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## Full Documentation

📖 **Complete Guides:**
- `MAP_FEATURE.md` - Detailed map documentation
- `IMPROVEMENTS.md` - Text parser enhancements
- `QUICK_REFERENCE.md` - Quick command reference
- `README.md` - Main documentation

🧪 **Test Scripts:**
- `test_map.py` - Generate sample maps
- `test_parser.py` - Test text parsing
- `demo.py` - Interactive demo

---

## Quick Commands Cheat Sheet

```powershell
# Activate venv
.\venv\Scripts\activate

# Start server
python -m app.main

# Generate map (in new terminal)
curl.exe -X POST http://localhost:8000/api/tourism/map -H "Content-Type: application/json" -d '{\"query\": \"Show me Paris\"}' -o paris.html

# Open map
start paris.html

# Test text query
curl.exe -X POST http://localhost:8000/api/tourism/query -H "Content-Type: application/json" -d '{\"query\": \"Weather in NYC?\"}'

# Check health
curl.exe http://localhost:8000/health
```

---

## Summary

✅ **Server is running**  
✅ **Maps are working**  
✅ **Sample maps generated**  
✅ **All features tested**

**Just open any `.html` file in the `backend` folder to see your interactive maps!**

🎉 **Enjoy your enhanced tourism system!** 🗺️✨
