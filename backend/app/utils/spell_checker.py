"""Spell checker for city/place names using fuzzy matching."""

from difflib import get_close_matches
from typing import List, Optional, Tuple
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


# Common world cities and tourist destinations (can be expanded)
COMMON_CITIES = [
    # India
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", 
    "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal",
    "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra",
    "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar",
    "Amritsar", "Chandigarh", "Jodhpur", "Guwahati", "Udaipur", "Goa", "Kerala",
    "Manali", "Shimla", "Rishikesh", "Haridwar", "Mysore", "Ooty", "Coorg",
    
    # International - Major cities
    "London", "Paris", "New York", "Tokyo", "Dubai", "Singapore", "Hong Kong",
    "Los Angeles", "Chicago", "San Francisco", "Las Vegas", "Miami", "Boston",
    "Seattle", "Washington", "Rome", "Barcelona", "Madrid", "Berlin", "Amsterdam",
    "Vienna", "Prague", "Budapest", "Athens", "Istanbul", "Cairo", "Bangkok",
    "Seoul", "Beijing", "Shanghai", "Sydney", "Melbourne", "Toronto", "Vancouver",
    "Montreal", "Mexico City", "Rio de Janeiro", "Buenos Aires", "Lima", "Bogota",
    "Moscow", "St Petersburg", "Lisbon", "Copenhagen", "Stockholm", "Oslo",
    "Helsinki", "Dublin", "Edinburgh", "Manchester", "Brussels", "Milan", "Venice",
    "Florence", "Naples", "Munich", "Frankfurt", "Zurich", "Geneva", "Marrakech",
    
    # Multi-word cities
    "New York City", "Los Angeles", "San Francisco", "Las Vegas", "Rio de Janeiro",
    "Buenos Aires", "Mexico City", "Cape Town", "Tel Aviv", "Kuala Lumpur",
    "Ho Chi Minh City", "Phnom Penh", "New Delhi", "Colombo", "Kathmandu"
]


class SpellChecker:
    """Spell checker for city/place names using fuzzy matching."""
    
    def __init__(self):
        """Initialize spell checker with city database."""
        self.cities = COMMON_CITIES
        self.logger = setup_logger(__name__)
        self.logger.info(f"Initialized spell checker with {len(self.cities)} cities")
    
    def suggest_correction(self, place_name: str, max_suggestions: int = 3) -> List[str]:
        """
        Suggest spelling corrections for a place name.
        
        Args:
            place_name: Input place name (potentially misspelled)
            max_suggestions: Maximum number of suggestions to return
        
        Returns:
            List of suggested corrections
        """
        if not place_name:
            return []
        
        # Use difflib for fuzzy matching
        # cutoff=0.6 means at least 60% similarity
        matches = get_close_matches(
            place_name,
            self.cities,
            n=max_suggestions,
            cutoff=0.6
        )
        
        if matches:
            self.logger.info(f"Spelling suggestions for '{place_name}': {matches}")
        
        return matches
    
    def check_and_correct(self, place_name: str, threshold: float = 0.80) -> Tuple[str, bool]:
        """
        Check spelling and auto-correct if confidence is high.
        
        Args:
            place_name: Input place name
            threshold: Confidence threshold for auto-correction (0.0-1.0)
        
        Returns:
            Tuple of (corrected_name, was_corrected)
        """
        # Check if exact match exists (case-insensitive)
        for city in self.cities:
            if city.lower() == place_name.lower():
                return city, False  # Exact match, no correction needed
        
        # Try fuzzy matching
        suggestions = self.suggest_correction(place_name, max_suggestions=1)
        
        if suggestions:
            best_match = suggestions[0]
            # Calculate similarity score
            from difflib import SequenceMatcher
            similarity = SequenceMatcher(None, place_name.lower(), best_match.lower()).ratio()
            
            if similarity >= threshold:
                self.logger.info(f"Auto-corrected '{place_name}' to '{best_match}' (confidence: {similarity:.2%})")
                return best_match, True
        
        # No correction found
        return place_name, False
