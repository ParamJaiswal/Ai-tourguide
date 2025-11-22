# Inkle Tourism System - Multi-Agent AI Tourism Assistant

A production-ready multi-agent tourism system that provides weather information and tourist attraction recommendations using external APIs. Built with FastAPI and enhanced with intelligent text parsing and spell correction.

## ✨ New Improvements (v2.0)

🎉 **Enhanced Text Parser with Smart Features:**
- ✅ **Automatic Spell Correction**: Fixes misspelled city names (e.g., "Banglore" → "Bangalore")
- ✅ **City Aliases Support**: Recognizes abbreviations (e.g., "NYC" → "New York", "LA" → "Los Angeles")
- ✅ **Natural Language Understanding**: Handles various query formats naturally
- ✅ **Helpful Suggestions**: Provides alternatives when location is unclear
- ✅ **200+ City Database**: Comprehensive coverage of world cities
- ✅ **Multi-word Location Support**: Handles "New York City", "San Francisco", etc.

🗺️ **NEW! Interactive Map Visualization:**
- ✅ **Beautiful Interactive Maps**: See tourist attractions marked on a map
- ✅ **Color-Coded Markers**: Different colors for museums, parks, monuments, etc.
- ✅ **Info Sidebar**: Weather + Attraction list with gradient design
- ✅ **Map Tools**: Fullscreen mode, distance measurement, zoom controls
- ✅ **Responsive Design**: Works perfectly on mobile and desktop
- ✅ **No API Keys Needed**: Uses free OpenStreetMap data

📖 **Documentation:**
- **IMPROVEMENTS.md** - Detailed text parser enhancements
- **MAP_FEATURE.md** - Complete map feature guide (NEW!)
- **QUICK_START.md** - Quick reference guide

## 🌟 Core Features

- **Multi-Agent Architecture**: Parent agent orchestrates specialized child agents (Weather & Places)
- **Enhanced Text Parsing**: Intelligent spell correction and natural language understanding
- **Interactive Maps**: Beautiful visual representation of cities and attractions (NEW!)
- **Weather Information**: Real-time weather data using Open-Meteo API
- **Tourist Attractions**: Up to 5 tourist spots with coordinates using Overpass API
- **Geocoding**: Place name to coordinates conversion with Nominatim API
- **Smart Error Handling**: Helpful suggestions and auto-correction feedback
- **Docker Ready**: Containerized deployment with docker-compose
- **No LLM APIs Required**: Uses rule-based logic instead of expensive LLM APIs

## 🏗️ Architecture

```
User Query → Parent Agent (Orchestrator)
                ↓
        Intent Detection
                ↓
    ┌───────────┴───────────┐
    ↓                       ↓
Weather Agent          Places Agent
    ↓                       ↓
Open-Meteo API      Overpass API
    ↓                       ↓
    └───────────┬───────────┘
                ↓
        Combined Response
```

### Components

- **Parent Agent**: Orchestrates the system using intent detection and place extraction
- **Weather Agent**: Fetches current temperature and precipitation probability
- **Places Agent**: Retrieves tourist attractions from OpenStreetMap data
- **Geocoding Service**: Converts place names to coordinates
- **FastAPI**: RESTful API with automatic documentation

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone and navigate to the project**:
   ```bash
   cd inkle-tourism-system
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Local Development

1. **Create a virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env file** (optional):
   ```bash
   copy .env.example .env
   ```

4. **Run the application**:
   ```bash
   # From backend directory
   python -m app.main
   
   # OR using uvicorn directly
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📖 API Usage

### Endpoint: `POST /api/tourism/query`

#### Example 1: Weather Query
```bash
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "I'\''m going to go to Bangalore, what is the temperature there?"}'
```

**Response**:
```json
{
  "success": true,
  "message": "In Bangalore it's currently 24.0°C with a chance of 35% to rain.",
  "place_name": "Bangalore",
  "coordinates": {"lat": 12.9716, "lon": 77.5946}
}
```

#### Example 2: Spell Correction (NEW!)
```bash
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What'\''s the weather in Banglore?"}'
```

**Response**:
```json
{
  "success": true,
  "message": "(I understood 'Banglore' as 'Bangalore') In Bangalore it's currently 24.0°C with a chance of 35% to rain.",
  "place_name": "Bangalore",
  "coordinates": {"lat": 12.9716, "lon": 77.5946}
}
```

#### Example 3: City Alias (NEW!)
```bash
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What can I see in NYC?"}'
```

**Response**:
```json
{
  "success": true,
  "message": "In New York these are the places you can go,\nTimes Square\nCentral Park\nStatue of Liberty\nEmpire State Building\nBrooklyn Bridge",
  "place_name": "New York",
  "coordinates": {"lat": 40.7128, "lon": -74.0060}
}
```

#### Example 4: Places Query
```bash
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What places can I visit in Bangalore?"}'
```

**Response**:
```json
{
  "success": true,
  "message": "In Bangalore these are the places you can go,\nLalbagh\nSri Chamarajendra Park\nBangalore Palace\nBannerghatta National Park\nJawaharlal Nehru Planetarium",
  "place_name": "Bangalore",
  "coordinates": {"lat": 12.9716, "lon": 77.5946}
}
```

#### Example 5: Combined Query
```bash
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "I am going to Paris, what is the temperature and what places can I visit?"}'
```

**Response**:
```json
{
  "success": true,
  "message": "In Paris it's currently 15.2°C with a chance of 20% to rain. And in Paris these are the places you can go,\nEiffel Tower\nLouvre Museum\nNotre-Dame Cathedral\nArc de Triomphe\nSacré-Cœur",
  "place_name": "Paris",
  "coordinates": {"lat": 48.8566, "lon": 2.3522}
}
```

#### Example 6: Non-existent Place with Suggestions (NEW!)
```bash
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to visit Parris"}'
```

**Response**:
```json
{
  "success": false,
  "message": "I couldn't find 'Parris'. Did you mean: Paris, Patras? Please try again with the correct spelling.",
  "place_name": null,
  "coordinates": null
}
```

#### Example 7: Interactive Map (NEW! 🗺️)
```bash
# Get an interactive map with attractions
curl -X POST http://localhost:8000/api/tourism/map \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me Paris"}' \
  > paris_map.html

# Then open paris_map.html in your browser!
```

**Features**:
- Interactive markers for each attraction
- Color-coded by type (museums, parks, monuments)
- Weather information in sidebar
- Fullscreen mode and distance measurement
- Responsive design for mobile

**What you'll see**:
- 📍 City center marked with red home icon
- ⭐ Tourist attractions with numbered markers
- 🎨 Beautiful gradient sidebar with info
- 🔧 Map tools (zoom, measure, fullscreen)

**Try these queries**:
```
"Map of Tokyo"
"Show attractions in London"
"Paris map with weather"
"Places in New York"
```

📖 **See [MAP_FEATURE.md](MAP_FEATURE.md) for complete map documentation!**

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory (use `.env.example` as template):

```env
# Logging
LOG_LEVEL=INFO

# API Configuration
API_TIMEOUT=30

# Application Settings
APP_NAME=Inkle Tourism System
APP_VERSION=1.0.0
```

### External APIs Used

All APIs are **free and require no authentication**:

- **Nominatim API**: Geocoding (1 req/sec rate limit enforced)
- **Open-Meteo API**: Weather forecasts
- **Overpass API**: OpenStreetMap tourist attractions

## 📁 Project Structure

```
inkle-tourism-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── models.py            # Pydantic models
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py    # Base agent class
│   │   │   ├── parent_agent.py  # Orchestrator (enhanced)
│   │   │   ├── weather_agent.py # Weather specialist
│   │   │   └── places_agent.py  # Places specialist
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── geocoding.py     # Nominatim integration
│   │   │   ├── weather.py       # Open-Meteo integration
│   │   │   └── places.py        # Overpass integration
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── text_parser.py   # Enhanced text parser (NEW!)
│   │       ├── nlp_processor.py # Original NLP processor
│   │       ├── spell_checker.py # Original spell checker
│   │       ├── logger.py        # Logging setup
│   │       └── exceptions.py    # Custom exceptions
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
├── .gitignore
├── README.md
├── IMPROVEMENTS.md               # Detailed improvement docs (NEW!)
└── SETUP.md
```

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Interactive API Documentation
Visit http://localhost:8000/docs to test the API interactively using Swagger UI.

## 🐛 Troubleshooting

### Rate Limiting Issues
If you receive too many geocoding requests, the system enforces a 1-second delay between Nominatim requests. This is automatic.

### Docker Build Issues
```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Port Already in Use
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Can't Find Places
The Overpass API searches within a 10km radius. For smaller cities or rural areas, results may be limited.

## 🚢 Deployment

### Production Considerations

1. **API Rate Limits**: Nominatim has a 1 req/sec limit (already implemented)
2. **CORS**: Update `allow_origins` in `main.py` to restrict origins
3. **Logging**: Set `LOG_LEVEL=WARNING` in production
4. **Health Checks**: Endpoint at `/health` for load balancers
5. **Scaling**: Consider caching geocoding results for popular places

### Docker Production Deployment

```bash
# Build production image
docker-compose -f docker-compose.yml build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📝 License

This project was created for the Inkle AI Intern assignment.

## 🤝 Contributing

This is an assignment project, but suggestions are welcome!

## 📧 Support

For issues or questions, please create an issue in the repository.

---

**Built with ❤️ using FastAPI, Python, and free open-source APIs**
