"""Lightweight NLP processor for intelligent query understanding (no external dependencies)."""

import re
from typing import Dict, List, Optional, Tuple
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NLPProcessor:
    """Intelligent NLP processor using advanced pattern matching and heuristics."""
    
    # Common location words/phrases in queries
    LOCATION_INDICATORS = [
        "going to", "visit", "visiting", "to", "in", "at", "near",
        "around", "from", "arrive", "arriving", "heading to", "travel to",
        "trip to", "vacation in", "holiday in", "about", "explore"
    ]
    
    # Weather-related terms
    WEATHER_TERMS = {
        "direct": ["weather", "temperature", "temp", "forecast", "climate"],
        "conditions": ["rain", "raining", "rainy", "sunny", "cloudy", "snow", "snowing"],
        "attributes": ["hot", "cold", "warm", "cool", "humid", "dry"],
        "questions": ["how hot", "how cold", "how warm", "what's the temperature"]
    }
    
    # Places-related terms  
    PLACES_TERMS = {
        "direct": ["places", "attractions", "tourist", "sightseeing", "landmarks", "destinations"],
        "actions": ["visit", "see", "explore", "tour", "check out", "go to", "do"],
        "questions": ["what to", "where to", "things to", "where can", "what can"]
    }
    
    # Common non-location words to filter out
    SKIP_WORDS = {
        "i", "im", "i'm", "what", "where", "how", "when", "why", "who",
        "the", "is", "are", "was", "were", "can", "could", "should", "would",
        "these", "those", "there", "here", "and", "or", "but", "if", "then"
    }
    
    def __init__(self):
        """Initialize NLP processor."""
        self.logger = setup_logger(__name__)
        self.logger.info("Initialized lightweight NLP processor")
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for processing."""
        # Convert to lowercase
        text = text.lower()
        # Normalize punctuation
        text = text.replace("'", "'").replace(""", '"').replace(""", '"')
        # Clean up extra spaces
        text = " ".join(text.split())
        return text
    
    def _extract_with_indicators(self, text: str) -> Optional[str]:
        """Extract location using indicator phrases."""
        text_lower = text.lower()
        
        for indicator in self.LOCATION_INDICATORS:
            pattern = rf"{re.escape(indicator)}\s+([a-z\s]+?)(?:\s*[,?.!]|$|\s+(?:what|where|how|and|or|the|is|are))"
            match = re.search(pattern, text_lower)
            if match:
                location = match.group(1).strip()
                # Capitalize
                location = " ".join(word.capitalize() for word in location.split())
                if location and len(location) > 2:
                    return location
        
        return None
    
    def _extract_proper_nouns(self, text: str) -> List[str]:
        """Extract potential proper nouns (capitalized words)."""
        # Find sequences of capitalized words
        pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        matches = re.findall(pattern, text)
        
        # Filter out skip words
        locations = []
        for match in matches:
            words = match.split()
            filtered = [w for w in words if w.lower() not in self.SKIP_WORDS]
            if filtered:
                locations.append(" ".join(filtered))
        
        return locations
    
    def _score_location_candidates(self, candidates: List[str]) -> Optional[str]:
        """Score and select best location candidate."""
        if not candidates:
            return None
        
        # Prefer longer, more specific names
        scored = [(loc, len(loc.split())) for loc in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return scored[0][0]
    
    def extract_location(self, text: str) -> Optional[str]:
        """
        Extract location/place name using advanced pattern matching.
        
        Args:
            text: Input query text
        
        Returns:
            Extracted location name or None
        """
        original_text = text
        
        # Method 1: Try indicator-based extraction (works with lowercase)
        location = self._extract_with_indicators(text)
        if location:
            self.logger.info(f"Extracted location via indicators: {location}")
            return location
        
        # Method 2: Try proper noun extraction (original text)
        proper_nouns = self._extract_proper_nouns(original_text)
        if proper_nouns:
            location = self._score_location_candidates(proper_nouns)
            if location:
                self.logger.info(f"Extracted location via proper nouns: {location}")
                return location
        
        # Method 3: Look for ANY capitalized word sequence after normalization
        # This handles cases like "tell me about Paris"
        words = text.split()
        for i, word in enumerate(words):
            if word and word[0].isupper() and word.lower() not in self.SKIP_WORDS:
                # Check if next words are also capitalized
                location_parts = [word]
                for j in range(i + 1, len(words)):
                    if words[j] and words[j][0].isupper():
                        location_parts.append(words[j])
                    else:
                        break
                
                location = " ".join(location_parts)
                if len(location) > 2:
                    self.logger.info(f"Extracted location via capitalization: {location}")
                    return location
        
        self.logger.warning(f"Could not extract location from: {text}")
        return None
    
    def _check_term_presence(self, text: str, term_dict: Dict[str, List[str]]) -> bool:
        """Check if any terms from dictionary are present in text."""
        text_lower = text.lower()
        
        for category, terms in term_dict.items():
            if any(term in text_lower for term in terms):
                return True
        
        return False
    
    def detect_intent(self, text: str) -> Dict[str, bool]:
        """
        Detect user intent using advanced pattern matching.
        
        Args:
            text: Input query text
        
        Returns:
            Dictionary with 'weather' and 'places' boolean flags
        """
        wants_weather = self._check_term_presence(text, self.WEATHER_TERMS)
        wants_places = self._check_term_presence(text, self.PLACES_TERMS)
        
        # Additional context-based detection
        text_lower = text.lower()
        
        # If asking "what" without places terms, likely wants places
        if "what" in text_lower and not wants_weather:
            if any(word in text_lower for word in ["can", "should", "do", "see"]):
                wants_places = True
        
        # If asking about going somewhere without specific intent, assume places
        if any(phrase in text_lower for phrase in ["going to", "heading to", "trip to", "visit"]):
            if not wants_weather:
                wants_places = True
        
        # Default to places if nothing detected
        if not wants_weather and not wants_places:
            wants_places = True
        
        intent = {
            "weather": wants_weather,
            "places": wants_places
        }
        
        self.logger.info(f"Detected intent: {intent}")
        return intent
    
    def preprocess_query(self, text: str) -> str:
        """
        Preprocess query text for better understanding.
        
        Args:
            text: Raw query text
        
        Returns:
            Preprocessed text
        """
        # Basic cleaning
        text = text.strip()
        
        # Normalize quotes and apostrophes
        text = text.replace("'", "'").replace(""", '"').replace(""", '"')
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        return text
    
    def analyze_query(self, query: str) -> Dict[str, any]:
        """
        Complete query analysis.
        
        Args:
            query: User query
        
        Returns:
            Dictionary with location, intent, and processed query
        """
        # Preprocess
        processed_query = self.preprocess_query(query)
        
        # Extract location
        location = self.extract_location(processed_query)
        
        # Detect intent
        intent = self.detect_intent(processed_query)
        
        result = {
            "location": location,
            "intent": intent,
            "original_query": query,
            "processed_query": processed_query
        }
        
        self.logger.info(f"Query analysis complete: location={location}, intent={intent}")
        return result
