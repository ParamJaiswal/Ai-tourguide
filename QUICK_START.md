# Quick Start Guide - Enhanced Tourism System

## What's New? 🎉

Your tourism system is now smarter! It can:
- ✅ Auto-correct spelling mistakes
- ✅ Understand abbreviations (NYC, LA, etc.)
- ✅ Handle natural language queries
- ✅ Provide helpful suggestions

## Examples of Queries That Work

### Weather Queries
```
"What's the weather in Banglore?"  → Auto-corrects to Bangalore
"Temperature in LA"                 → Recognizes as Los Angeles
"How hot is it in Parris?"         → Auto-corrects to Paris
"I'm going to Tokyo tomorrow"      → Extracts Tokyo
```

### Places Queries
```
"What can I see in NYC?"           → Recognizes as New York
"Places to visit in Rome"          → Extracts Rome
"Things to do in San Francisco"    → Extracts San Francisco
"Tell me about Dubai"              → Extracts Dubai
```

### Combined Queries (Weather + Places)
```
"I'm visiting Tokyo, what's the weather and what can I see?"
"Tell me about Dubai weather and attractions"
"Going to Paris, what's the temp and what places to visit?"
```

## How to Test

### Method 1: Using the Test Script
```bash
cd backend
python test_parser.py
```

### Method 2: Using Python Directly
```bash
cd backend
python -c "
from app.utils.text_parser import EnhancedTextParser
parser = EnhancedTextParser()
result = parser.parse_query('What is the weather in Banglore?')
print(f'Location: {result[\"location\"]}')
print(f'Corrected: {result[\"was_corrected\"]}')
print(f'Intent: {result[\"intent\"]}')
"
```

### Method 3: Start the API Server
```bash
# From the backend directory
python -m app.main

# Or using uvicorn
uvicorn app.main:app --reload
```

Then test with curl:
```bash
# Test spell correction
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in Banglore?"}'

# Test alias recognition
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Places to visit in NYC"}'

# Test natural language
curl -X POST http://localhost:8000/api/tourism/query \
  -H "Content-Type: application/json" \
  -d '{"query": "I am heading to Tokyo tomorrow, what should I pack?"}'
```

### Method 4: Use Swagger UI
1. Start the server
2. Open http://localhost:8000/docs
3. Try the `/api/tourism/query` endpoint with various queries

## Common Test Cases

### Spell Correction
- "Banglore" → "Bangalore"
- "Parris" → "Paris"
- "Londan" → "London"
- "Tokio" → "Tokyo"

### City Aliases
- "NYC" → "New York"
- "LA" → "Los Angeles"
- "SF" → "San Francisco"
- "DC" → "Washington"
- "Bombay" → "Mumbai"

### Natural Language Understanding
- "I'm going to X" → Extracts X
- "What can I see in X?" → Extracts X
- "Tell me about X weather" → Extracts X
- "Heading to X tomorrow" → Extracts X

## Expected Responses

### Success with Correction:
```json
{
  "success": true,
  "message": "(I understood 'Banglore' as 'Bangalore') In Bangalore it's currently 24.0°C...",
  "place_name": "Bangalore",
  "coordinates": {"lat": 12.9716, "lon": 77.5946}
}
```

### Success with Alias:
```json
{
  "success": true,
  "message": "In New York these are the places you can go...",
  "place_name": "New York",
  "coordinates": {"lat": 40.7128, "lon": -74.0060}
}
```

### Error with Suggestions:
```json
{
  "success": false,
  "message": "I couldn't find 'Parris'. Did you mean: Paris, Patras? Please try again...",
  "place_name": null,
  "coordinates": null
}
```

## Troubleshooting

### Location Not Recognized
If a city isn't recognized, it might not be in the database. You can:
1. Add it to `WORLD_CITIES` list in `text_parser.py`
2. Add an alias in `LOCATION_ALIASES` dictionary
3. Make sure it's spelled correctly (or close enough for fuzzy matching)

### Intent Not Detected Correctly
The system looks for keywords. Make sure your query includes:
- For weather: "weather", "temperature", "hot", "cold", etc.
- For places: "places", "visit", "see", "attractions", etc.

### Server Not Starting
```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment if using one
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python -m app.main
```

## Next Steps

1. **Test the improvements**: Run the test script to see all features
2. **Try your own queries**: Use natural language, misspellings, and aliases
3. **Read IMPROVEMENTS.md**: For detailed technical documentation
4. **Deploy**: Use Docker or deploy to your preferred platform

## Need Help?

- Check the logs for detailed information
- Read IMPROVEMENTS.md for implementation details
- Review the test cases in test_parser.py
- Check the main README.md for API documentation

---

Happy Testing! 🚀
