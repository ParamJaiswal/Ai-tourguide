"""Enhanced text parser with spell correction and intelligent query understanding."""

import re
from typing import Dict, List, Optional, Tuple
from difflib import get_close_matches, SequenceMatcher
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


# Comprehensive list of world cities and tourist destinations
WORLD_CITIES = [
    # India - Major cities and tourist destinations
    "Mumbai", "Delhi", "Bangalore", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", 
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal",
    "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra",
    "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar",
    "Amritsar", "Chandigarh", "Jodhpur", "Guwahati", "Udaipur", "Goa", "Kerala",
    "Manali", "Shimla", "Rishikesh", "Haridwar", "Mysore", "Ooty", "Coorg",
    "Darjeeling", "Ladakh", "Pondicherry", "Hampi", "Khajuraho", "Kochi",
    
    # USA
    "New York", "New York City", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "San Francisco", "Charlotte", "Indianapolis",
    "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville",
    "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville",
    "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento",
    "Kansas City", "Mesa", "Atlanta", "Omaha", "Colorado Springs", "Raleigh",
    "Miami", "Virginia Beach", "Oakland", "Minneapolis", "Tulsa", "Arlington",
    
    # Europe
    "London", "Paris", "Berlin", "Madrid", "Rome", "Barcelona", "Vienna",
    "Hamburg", "Munich", "Milan", "Prague", "Budapest", "Warsaw", "Brussels",
    "Amsterdam", "Stockholm", "Copenhagen", "Oslo", "Helsinki", "Dublin",
    "Athens", "Lisbon", "Edinburgh", "Manchester", "Lyon", "Marseille",
    "Turin", "Palermo", "Seville", "Zaragoza", "Valencia", "Krakow",
    "Glasgow", "Venice", "Florence", "Naples", "Geneva", "Zurich",
    
    # Asia
    "Tokyo", "Shanghai", "Beijing", "Seoul", "Hong Kong", "Singapore",
    "Bangkok", "Jakarta", "Manila", "Ho Chi Minh City", "Kuala Lumpur",
    "Taipei", "Hanoi", "Osaka", "Busan", "Phnom Penh", "Yangon", "Colombo",
    "Kathmandu", "Dhaka", "Karachi", "Lahore", "Islamabad", "Kabul",
    
    # Middle East & Africa
    "Dubai", "Abu Dhabi", "Riyadh", "Jeddah", "Tehran", "Baghdad", "Amman",
    "Beirut", "Damascus", "Jerusalem", "Tel Aviv", "Cairo", "Alexandria",
    "Casablanca", "Marrakech", "Tunis", "Algiers", "Cape Town", "Johannesburg",
    "Nairobi", "Lagos", "Addis Ababa", "Dar es Salaam", "Accra", "Khartoum",
    
    # Oceania
    "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast",
    "Canberra", "Auckland", "Wellington", "Christchurch",
    
    # Latin America
    "Mexico City", "São Paulo", "Buenos Aires", "Rio de Janeiro", "Lima",
    "Bogotá", "Santiago", "Caracas", "Quito", "Montevideo", "Havana",
    "Panama City", "San Juan", "Guadalajara", "Monterrey",
]


# Common location misspellings and variations
LOCATION_ALIASES = {
    "ny": "New York",
    "nyc": "New York",
    "sf": "San Francisco",
    "la": "Los Angeles",
    "dc": "Washington",
    "chi": "Chicago",
    "philly": "Philadelphia",
    "vegas": "Las Vegas",
    "mumbai": "Mumbai",
    "bombay": "Mumbai",
    "calcutta": "Kolkata",
    "madras": "Chennai",
    "banglore": "Bangalore",
    "bengaluru": "Bangalore",
}


class EnhancedTextParser:
    """
    Enhanced text parser with spell correction and intelligent query understanding.
    Handles:
    - Automatic spell correction for city names
    - Multi-word location extraction
    - Intent detection (weather, places, both)
    - Query preprocessing and normalization
    """
    
    # Location indicators in natural language
    LOCATION_PATTERNS = [
        # Going/visiting patterns
        r"(?:going|heading|traveling|travelling|fly(?:ing)?)\s+to\s+([a-zA-Z\s]+?)(?:\s*[,?.!]|$|\s+(?:what|where|how|and|or|for))",
        r"(?:visit|visiting|explore|exploring|tour|touring)\s+([a-zA-Z\s]+?)(?:\s*[,?.!]|$|\s+(?:what|where|how|and|or))",
        
        # Location context patterns
        r"(?:in|at|near|around)\s+([a-zA-Z\s]+?)(?:\s*[,?.!]|$|\s+(?:what|where|how|and|or|the|is|are))",
        r"(?:to|about)\s+([a-zA-Z\s]+?)(?:\s*[,?.!]|$|\s+(?:what|where|how|and|or))",
        
        # Trip/vacation patterns
        r"(?:trip|vacation|holiday|tour)\s+(?:to|in)\s+([a-zA-Z\s]+?)(?:\s*[,?.!]|$|\s+(?:what|where|how|and|or))",
        
        # Weather-specific patterns
        r"(?:weather|temperature|climate)\s+(?:in|at|of)\s+([a-zA-Z\s]+?)(?:\s*[,?.!]|$)",
        r"([a-zA-Z\s]+?)\s+(?:weather|temperature|climate)(?:\s*[,?.!]|$)",
        
        # Places-specific patterns
        r"(?:places|attractions|sights)\s+(?:in|at|around|near)\s+([a-zA-Z\s]+?)(?:\s*[,?.!]|$)",
    ]
    
    # Weather-related keywords
    WEATHER_KEYWORDS = [
        "weather", "temperature", "temp", "forecast", "climate", "celsius", "fahrenheit",
        "rain", "raining", "rainy", "sunny", "cloudy", "cloud", "snow", "snowing",
        "hot", "cold", "warm", "cool", "humid", "dry", "windy", "wind",
        "how hot", "how cold", "how warm", "degrees"
    ]
    
    # Places-related keywords
    PLACES_KEYWORDS = [
        "places", "attractions", "tourist", "sightseeing", "landmarks", "destinations",
        "visit", "see", "explore", "tour", "check out", "things to do",
        "what to", "where to", "where can", "what can", "sights", "monuments",
        "museums", "parks", "restaurants", "hotels", "shopping"
    ]
    
    # Words to skip when extracting locations
    SKIP_WORDS = {
        "i", "im", "i'm", "me", "my", "what", "where", "how", "when", "why", "who",
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "can", "could", "should", "would", "will", "shall", "may", "might",
        "these", "those", "there", "here", "this", "that",
        "and", "or", "but", "if", "then", "so", "for", "to", "of", "in", "on", "at",
        "do", "does", "did", "have", "has", "had", "go", "going", "want", "need",
        # Additional temporal and action words
        "today", "tomorrow", "yesterday", "tonight", "now", "later", "soon",
        "next", "week", "month", "year", "day", "morning", "evening", "afternoon",
        "weather", "temperature", "climate", "temp", "forecast",
        "see", "visit", "visiting", "explore", "check", "tell", "show",
        "city", "place", "places", "about", "attractions", "tomorow",  # common typo
    }
    
    def __init__(self):
        """Initialize the enhanced text parser."""
        self.cities = WORLD_CITIES
        self.aliases = LOCATION_ALIASES
        self.logger = setup_logger(__name__)
        self.logger.info(f"Initialized enhanced text parser with {len(self.cities)} cities")
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for better processing.
        
        Args:
            text: Input text
        
        Returns:
            Normalized text
        """
        # Convert to lowercase for processing
        text = text.lower()
        
        # Normalize quotes and apostrophes
        text = text.replace("'", "'").replace(""", '"').replace(""", '"')
        text = text.replace("'", "'")
        
        # Fix common contractions
        text = text.replace("i'm", "i am")
        text = text.replace("im ", "i am ")
        text = text.replace("whats", "what is")
        text = text.replace("what's", "what is")
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        return text
    
    def fix_common_typos(self, text: str) -> str:
        """
        Fix common typos and misspellings.
        
        Args:
            text: Input text
        
        Returns:
            Text with typos fixed
        """
        # Common typos
        typo_map = {
            r'\bweather\b': 'weather',
            r'\btemprature\b': 'temperature',
            r'\btemperture\b': 'temperature',
            r'\bwether\b': 'weather',
            r'\bwhether\b': 'weather',  # Common confusion
            r'\bvisit\b': 'visit',
            r'\bplaces\b': 'places',
            r'\bplacez\b': 'places',
        }
        
        for pattern, replacement in typo_map.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def check_city_spelling(self, city_name: str) -> Tuple[str, bool, List[str]]:
        """
        Check and correct city name spelling.
        
        Args:
            city_name: Input city name
        
        Returns:
            Tuple of (corrected_name, was_corrected, suggestions)
        """
        if not city_name:
            return city_name, False, []
        
        # Check aliases first
        city_lower = city_name.lower()
        if city_lower in self.aliases:
            return self.aliases[city_lower], True, []
        
        # Check for exact match (case-insensitive)
        for city in self.cities:
            if city.lower() == city_lower:
                return city, False, []
        
        # Try fuzzy matching
        matches = get_close_matches(city_name, self.cities, n=3, cutoff=0.6)
        
        if matches:
            best_match = matches[0]
            # Calculate similarity
            similarity = SequenceMatcher(None, city_lower, best_match.lower()).ratio()
            
            # Auto-correct if similarity is high (80% or more)
            if similarity >= 0.80:
                self.logger.info(f"Auto-corrected '{city_name}' to '{best_match}' (similarity: {similarity:.2%})")
                return best_match, True, matches
            else:
                # Return suggestions without auto-correcting
                self.logger.info(f"Suggestions for '{city_name}': {matches}")
                return city_name, False, matches
        
        return city_name, False, []
    
    def extract_location(self, text: str) -> Optional[Tuple[str, bool, List[str]]]:
        """
        Extract location from text using pattern matching and spell correction.
        
        Args:
            text: Input query text
        
        Returns:
            Tuple of (location, was_corrected, suggestions) or None
        """
        original_text = text
        normalized = self.normalize_text(text)
        
        # Try each location pattern
        for pattern in self.LOCATION_PATTERNS:
            match = re.search(pattern, normalized, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                
                # Clean up the extracted location
                location_words = location.split()
                filtered_words = [w for w in location_words if w.lower() not in self.SKIP_WORDS]
                
                if filtered_words:
                    location = " ".join(filtered_words)
                    # Capitalize properly
                    location = " ".join(word.capitalize() for word in location.split())
                    
                    # Check spelling and get corrections
                    corrected, was_corrected, suggestions = self.check_city_spelling(location)
                    
                    if corrected and len(corrected) > 2:
                        self.logger.info(f"Extracted location: {corrected} (original: {location})")
                        return corrected, was_corrected, suggestions
        
        # Try to find capitalized words in original text (backup method)
        words = original_text.split()
        potential_locations = []
        
        for i, word in enumerate(words):
            if word and word[0].isupper() and word.lower() not in self.SKIP_WORDS:
                # Check for multi-word locations
                location_parts = [word]
                
                for j in range(i + 1, min(i + 3, len(words))):
                    next_word = words[j]
                    # Only add if it's capitalized AND not a skip word AND not a common word
                    if (next_word and next_word[0].isupper() and 
                        next_word.lower() not in self.SKIP_WORDS and
                        not any(kw in next_word.lower() for kw in self.WEATHER_KEYWORDS) and
                        not any(kw in next_word.lower() for kw in self.PLACES_KEYWORDS)):
                        location_parts.append(next_word)
                    else:
                        break
                
                location = " ".join(location_parts)
                potential_locations.append(location)
        
        # Check all potential locations and return the first valid one
        for location in potential_locations:
            corrected, was_corrected, suggestions = self.check_city_spelling(location)
            
            if corrected and len(corrected) > 2:
                self.logger.info(f"Extracted location from capitalization: {corrected}")
                return corrected, was_corrected, suggestions
        
        # FALLBACK: Try to match any word in the query against city database (case-insensitive)
        # This handles lowercase city names like "mumbai", "paris", etc.
        words = normalized.split()
        for word in words:
            if word.lower() not in self.SKIP_WORDS and len(word) > 2:
                # Try as single word
                corrected, was_corrected, suggestions = self.check_city_spelling(word.capitalize())
                if corrected and len(corrected) > 2:
                    self.logger.info(f"Extracted location from word match: {corrected} (from: {word})")
                    return corrected, True, suggestions
        
        # Try multi-word combinations from normalized text
        words = normalized.split()
        for i in range(len(words)):
            for j in range(i + 1, min(i + 4, len(words) + 1)):
                phrase = " ".join(words[i:j])
                if len(phrase) > 3 and not all(w in self.SKIP_WORDS for w in phrase.split()):
                    # Capitalize each word
                    capitalized_phrase = " ".join(word.capitalize() for word in phrase.split())
                    corrected, was_corrected, suggestions = self.check_city_spelling(capitalized_phrase)
                    if corrected and len(corrected) > 2:
                        self.logger.info(f"Extracted location from phrase: {corrected} (from: {phrase})")
                        return corrected, True, suggestions
        
        self.logger.warning(f"Could not extract location from: {text}")
        return None
    
    def detect_intent(self, text: str) -> Dict[str, bool]:
        """
        Detect user intent from query with tourist guide intelligence.
        
        Args:
            text: Input query
        
        Returns:
            Dictionary with 'weather' and 'places' boolean flags
        """
        text_lower = text.lower()
        
        # Check for weather keywords
        wants_weather = any(keyword in text_lower for keyword in self.WEATHER_KEYWORDS)
        
        # Check for places keywords
        wants_places = any(keyword in text_lower for keyword in self.PLACES_KEYWORDS)
        
        # Check for map keywords
        wants_map = any(phrase in text_lower for phrase in ["map", "show me", "visualize", "display"])
        if wants_map:
            wants_places = True  # Map implies wanting to see places
        
        # Context-based detection
        if "what" in text_lower and not wants_weather:
            if any(word in text_lower for word in ["can", "should", "do", "see", "visit"]):
                wants_places = True
        
        # If asking about going somewhere without specific intent, default to places
        if any(phrase in text_lower for phrase in ["going to", "visiting", "trip to", "heading to", "travel to", "fly to"]):
            if not wants_weather:
                wants_places = True
        
        # Tourist guide mode: If query is VERY SHORT (likely just city name)
        # Default to showing places (tourist guide behavior)
        words_count = len([w for w in text_lower.split() if w.lower() not in self.SKIP_WORDS])
        if words_count <= 2 and not wants_weather:
            # Very short query like "Bangalore" or "Paris France" -> show places
            wants_places = True
            self.logger.info(f"Short query detected ({words_count} words) - activating tourist guide mode")
        
        # If nothing detected but query has minimal words, assume tourist guide mode
        if not wants_weather and not wants_places and words_count <= 3:
            wants_places = True
            self.logger.info("Minimal query - defaulting to tourist guide mode (places)")
        
        intent = {
            "weather": wants_weather,
            "places": wants_places
        }
        
        self.logger.info(f"Detected intent: {intent}")
        return intent
    
    def parse_query(self, query: str) -> Dict[str, any]:
        """
        Complete query parsing with spell correction and intent detection.
        
        Args:
            query: User query
        
        Returns:
            Dictionary with parsed information:
            - location: Extracted (and possibly corrected) location
            - was_corrected: Whether location was auto-corrected
            - suggestions: Alternative location suggestions (if any)
            - intent: Dictionary with weather/places flags
            - original_query: Original query text
            - processed_query: Cleaned/normalized query
        """
        # Clean up the query
        processed_query = query.strip()
        processed_query = self.fix_common_typos(processed_query)
        
        # Extract location with spell checking
        location_result = self.extract_location(processed_query)
        
        if location_result:
            location, was_corrected, suggestions = location_result
        else:
            location, was_corrected, suggestions = None, False, []
        
        # Detect intent
        intent = self.detect_intent(processed_query)
        
        result = {
            "location": location,
            "was_corrected": was_corrected,
            "suggestions": suggestions,
            "intent": intent,
            "original_query": query,
            "processed_query": processed_query
        }
        
        self.logger.info(f"Query parsed: location={location}, corrected={was_corrected}, intent={intent}")
        return result
