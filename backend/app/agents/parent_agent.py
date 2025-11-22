"""Parent agent for orchestrating tourism queries with enhanced text parsing."""

from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.agents.weather_agent import WeatherAgent
from app.agents.places_agent import PlacesAgent
from app.services.geocoding import get_coordinates
from app.utils.text_parser import EnhancedTextParser
from app.utils.exceptions import PlaceNotFoundError, GeocodingAPIError


class ParentAgent(BaseAgent):
    """Parent orchestrator agent that coordinates child agents using enhanced text parsing."""
    
    def __init__(self):
        super().__init__("parent")
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
        self.text_parser = EnhancedTextParser()
        self.logger.info("Initialized parent agent with enhanced text parser")
    
    async def process(self, query: str) -> Dict[str, Any]:
        """
        Process tourism query by coordinating child agents using enhanced text parsing.
        
        Args:
            query: User query text
        
        Returns:
            Formatted response from appropriate agents
        """
        try:
            self.logger.info(f"Processing query: {query}")
            
            # Parse query using enhanced text parser
            parsed = self.text_parser.parse_query(query)
            
            location = parsed["location"]
            intent = parsed["intent"]
            was_corrected = parsed["was_corrected"]
            suggestions = parsed["suggestions"]
            
            if not location:
                return self.format_response(
                    success=False,
                    data={
                        "text": "I couldn't identify a location in your query. Please mention a city or place you'd like to know about. For example: 'What's the weather in Paris?' or 'Places to visit in Tokyo'"
                    }
                )
            
            # Geocode the place
            try:
                coordinates = await get_coordinates(location)
                lat = coordinates["lat"]
                lon = coordinates["lon"]
                
                # Build correction note if location was auto-corrected
                correction_note = ""
                if was_corrected:
                    correction_note = f"(I understood '{parsed['original_query'].split()[-1]}' as '{location}') "
                    self.logger.info(f"Auto-corrected to: {location}")
                    
            except PlaceNotFoundError as e:
                # If we have suggestions from our enhanced parser, use them
                if suggestions:
                    suggestion_text = ", ".join(suggestions)
                    return self.format_response(
                        success=False,
                        data={
                            "text": f"I couldn't find '{location}'. Did you mean: {suggestion_text}? Please try again with the correct spelling."
                        }
                    )
                else:
                    return self.format_response(
                        success=False,
                        data={
                            "text": f"I couldn't find a place called '{location}'. Please check the spelling or try a different location."
                        }
                    )
            except GeocodingAPIError as e:
                return self.format_response(
                    success=False,
                    data={
                        "text": f"I couldn't locate '{location}' at the moment. Please try again later."
                    }
                )
            
            # Collect responses from relevant agents based on detected intent
            responses = []
            weather_data = None
            places_data = []
            
            # Smart default: If no specific intent detected, show places (tourist guide mode)
            # This makes it more helpful when user just says a city name
            if not intent["weather"] and not intent["places"]:
                self.logger.info(f"No specific intent - defaulting to tourist guide mode for {location}")
                intent["places"] = True  # Auto-show places
            
            if intent["weather"]:
                self.logger.info(f"Invoking weather agent for {location}")
                weather_response = await self.weather_agent.process(lat, lon, location)
                if weather_response["success"]:
                    responses.append(weather_response["data"]["text"])
                    # Store weather data for map
                    weather_data = {
                        "temp": weather_response["data"].get("temperature"),
                        "precipitation": weather_response["data"].get("precipitation")
                    }
            
            if intent["places"]:
                self.logger.info(f"Invoking places agent for {location}")
                places_response = await self.places_agent.process(lat, lon, location)
                if places_response["success"]:
                    responses.append(places_response["data"]["text"])
                    # Store places data for map
                    places_data = places_response["data"].get("places", [])
            
            # Combine responses with tourist guide personality
            if responses:
                # Handle combined responses with proper formatting
                if len(responses) == 2:
                    # Weather + Places
                    final_text = correction_note + responses[0].rstrip('.') + ". And " + responses[1][0].lower() + responses[1][1:]
                elif len(responses) == 1 and intent["places"] and not intent["weather"]:
                    # Just places - add friendly tourist guide intro
                    if correction_note:
                        final_text = correction_note + f"Great choice! {responses[0]}"
                    else:
                        final_text = f"Welcome to {location}! {responses[0]}"
                    
                    # Add helpful suggestions
                    if places_data:
                        final_text += f"\n\n💡 Would you like to know the weather in {location}? Or see these places on an interactive map? Just ask!"
                else:
                    final_text = correction_note + responses[0]
                
                return self.format_response(
                    success=True,
                    data={
                        "text": final_text,
                        "place_name": location,
                        "coordinates": coordinates,
                        "places": places_data,  # For map generation
                        "weather": weather_data  # For map generation
                    }
                )
            else:
                # Fallback with helpful suggestions
                return self.format_response(
                    success=True,
                    data={
                        "text": f"I can help you explore {location}! Ask me about:\n• Weather and temperature\n• Top tourist attractions\n• Interactive map view\n\nWhat would you like to know?",
                        "place_name": location,
                        "coordinates": coordinates
                    }
                )
                
        except Exception as e:
            self.logger.error(f"Unexpected error in parent agent: {str(e)}")
            return self.format_response(
                success=False,
                data={
                    "text": f"An error occurred while processing your request: {str(e)}"
                }
            )
