# 🎨 Tourism Guide - Frontend

## Beautiful, Modern Web Interface

A stunning single-page application for the Tourism Guide system with:
- ✨ Modern gradient design
- 🗺️ Interactive map integration
- 💬 Real-time query responses
- 📱 Fully responsive
- 🎯 Example queries for new users

---

## Features

### 1. **Smart Search**
- Type any city name or query
- Get instant AI-powered responses
- Auto-corrects typos

### 2. **Interactive Map**
- See tourist attractions marked on the map
- Color-coded markers by type
- Click markers for details

### 3. **Example Queries**
Pre-loaded examples to help new users:
- Paris
- Bangalore
- Weather in Tokyo
- Places in New York
- London weather and places
- Show me Dubai on map

### 4. **Beautiful UI**
- Purple gradient theme
- Smooth animations
- Toast notifications
- Loading states

---

## How to Run

### Option 1: Simple Python Server (Recommended)

```bash
# Navigate to frontend folder
cd frontend

# Start server (Python 3)
python -m http.server 8080

# Or if python3 specifically
python3 -m http.server 8080
```

Then open: **http://localhost:8080**

### Option 2: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 3: Double-Click

Simply double-click `index.html` to open in your browser!

**Note:** Some features might not work with file:// protocol. Use one of the server options for best results.

---

## Prerequisites

**Backend Server Must Be Running!**

```bash
# In a separate terminal
cd backend
.\venv\Scripts\activate
python -m app.main
```

Backend will run on: **http://localhost:8000**

---

## Usage

### 1. **Basic Query**
```
Type: "Paris"
Result: Get exciting places in Paris + map view
```

### 2. **Weather Query**
```
Type: "Weather in Tokyo"
Result: Weather info with clothing suggestions
```

### 3. **Combined Query**
```
Type: "London weather and places"
Result: Both weather and places + map
```

### 4. **With Typos**
```
Type: "Banglore"
Result: Auto-corrects to "Bangalore"
```

### 5. **Map View**
```
Type: "Show me Dubai on map"
Result: Interactive map with attractions
```

---

## Architecture

```
┌─────────────────┐
│   Frontend      │
│  (index.html)   │
│                 │
│  - User Input   │
│  - Display      │
│  - Map View     │
└────────┬────────┘
         │ HTTP
         │ POST /api/tourism/query
         ↓
┌─────────────────┐
│   Backend       │
│  (FastAPI)      │
│                 │
│  - Text Parser  │
│  - Agents       │
│  - APIs         │
└─────────────────┘
```

---

## Technology Stack

### Frontend
- **Pure HTML/CSS/JavaScript** - No framework needed!
- **Leaflet.js** - Interactive maps
- **Font Awesome** - Beautiful icons
- **Google Fonts** - Poppins font family

### Design
- Gradient background (Purple theme)
- Responsive grid layout
- Modern card-based UI
- Smooth animations

---

## File Structure

```
frontend/
├── index.html          # Main application
└── README.md           # This file
```

Everything in one file for simplicity!

---

## Customization

### Change Theme Colors

Edit the gradient in `index.html`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Change `#667eea` and `#764ba2` to your preferred colors.

### Change Backend URL

Edit the `API_URL` constant:

```javascript
const API_URL = 'http://localhost:8000';  // Change port if needed
```

### Add More Examples

Add chips in the HTML:

```html
<div class="chip" onclick="setQuery('Your Query')">Your Text</div>
```

---

## Responsive Design

Works perfectly on:
- 💻 Desktop (1920x1080+)
- 💻 Laptop (1366x768+)
- 📱 Tablet (768x1024)
- 📱 Mobile (375x667+)

---

## Browser Support

- ✅ Chrome (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ⚠️ IE11 (Not supported)

---

## Features in Detail

### Map Integration
- **Leaflet.js** for interactive maps
- OpenStreetMap tiles (free!)
- Color-coded markers:
  - 🔴 Red: City center
  - 🟣 Violet: Museums
  - 🟢 Green: Parks
  - 🔵 Blue: Monuments
  - 🟡 Gold: General attractions

### Response Display
- Preserves formatting
- Shows emojis properly
- Scrollable for long responses
- Loading states

### Error Handling
- Connection errors
- API errors
- User-friendly messages
- Toast notifications

---

## Example Queries

Try these to explore features:

**Simple:**
- `Paris`
- `Tokyo`
- `Bangalore`

**Weather:**
- `Weather in London`
- `Temperature in New York`
- `How hot is Dubai`

**Places:**
- `Places in Rome`
- `What can I see in Bangkok`
- `Attractions in Mumbai`

**Combined:**
- `Paris weather and places`
- `Tell me about Tokyo`

**With Typos:**
- `Banglore` (corrects to Bangalore)
- `Parris` (corrects to Paris)
- `Londan` (corrects to London)

---

## Troubleshooting

### Map Not Loading?
- Check internet connection
- Verify OpenStreetMap is accessible
- Check browser console for errors

### Backend Connection Error?
```
Error: Failed to get response
```

**Solution:**
1. Ensure backend is running: `python -m app.main`
2. Check backend URL in code
3. Verify CORS is enabled in backend

### Styling Issues?
- Clear browser cache
- Try incognito/private mode
- Check browser console

---

## Development

### Local Development
```bash
# Start backend
cd backend
python -m app.main

# Start frontend
cd frontend
python -m http.server 8080
```

### Making Changes
1. Edit `index.html`
2. Refresh browser
3. No build step needed!

---

## Deployment

### Deploy Frontend

**Option 1: GitHub Pages**
1. Push `frontend/index.html` to GitHub
2. Enable GitHub Pages
3. Update `API_URL` to production backend

**Option 2: Netlify/Vercel**
1. Drag and drop `frontend` folder
2. Update `API_URL`
3. Deploy!

**Option 3: With Backend**
1. Copy `index.html` to `backend/static/`
2. Serve via FastAPI static files

### Environment Variables
Update `API_URL` based on environment:
```javascript
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'
    : 'https://your-backend.com';
```

---

## Performance

- ⚡ **Fast:** Single file, minimal dependencies
- 📦 **Light:** ~20KB HTML (uncompressed)
- 🚀 **Quick Load:** CDN resources cached
- 💾 **Efficient:** Minimal HTTP requests

---

## Security

- ✅ No sensitive data stored
- ✅ HTTPS recommended for production
- ✅ CORS properly configured
- ✅ Input sanitization via backend

---

## Future Enhancements

Potential additions:
- [ ] Dark mode toggle
- [ ] Search history
- [ ] Favorite locations
- [ ] Share results
- [ ] Download map as image
- [ ] Multi-language support

---

## Support

**Issues?**
1. Check backend is running
2. Verify API URL is correct
3. Check browser console
4. Test with example queries

**Questions?**
- See main project README
- Check backend documentation
- Review code comments

---

## Credits

**Design Inspiration:**
- Modern SaaS applications
- Travel websites
- Map applications

**Libraries:**
- Leaflet.js - Maps
- Font Awesome - Icons
- Google Fonts - Typography

---

## License

Part of the Tourism Guide project.

---

**Enjoy your beautiful tourism guide!** 🌍✨
