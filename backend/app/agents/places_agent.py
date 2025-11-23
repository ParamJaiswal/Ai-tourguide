"""Places agent for handling tourist attraction queries."""

from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.services.places import get_tourist_attractions
from app.utils.exceptions import PlacesAPIError


class PlacesAgent(BaseAgent):
    """Agent specialized in tourist attractions."""
    
    def __init__(self):
        super().__init__("places")
    
    async def process(self, lat: float, lon: float, place_name: str) -> Dict[str, Any]:
        """
        Get tourist attractions for coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            place_name: Name of the place (for response formatting)
        
        Returns:
            Formatted places response with coordinates
        """
        try:
            self.logger.info(f"Processing places request for {place_name}")
            
            attractions = await get_tourist_attractions(lat, lon)
            
            # Format natural language response
            if attractions:
                # Extract just names for text response
                place_names = [place['name'] for place in attractions]
                
                # More engaging tourist guide response
                response_text = f"🌟 Exciting places to visit in {place_name}:\n\n"
                
                # Add numbered list with emojis
                for idx, place in enumerate(attractions, 1):
                    icon = "🏛️" if place.get('type') == 'museum' else \
                           "🌳" if place.get('type') == 'park' else \
                           "🏰" if place.get('type') in ['monument', 'castle'] else \
                           "👁️" if place.get('type') == 'viewpoint' else "⭐"
                    response_text += f"{idx}. {icon} {place['name']}\n"
                
                # Add helpful context
                response_text += f"\n💡 Tip: Ask me 'Show me {place_name} on a map' for an interactive view!"
                
            else:
                # More helpful message when no places found
                response_text = (
                    f"🤔 Hmm, I couldn't find popular tourist attractions listed for {place_name} in the database.\n\n"
                    f"This might be a smaller location or the data isn't available yet.\n"
                    f"💡 Try searching for:\n"
                    f"• Nearby major cities\n"
                    f"• Popular tourist destinations\n"
                    f"• Specific landmarks you're interested in"
                )
                attractions = []
            
            return self.format_response(
                success=True,
                data={
                    "text": response_text,
                    "places": attractions,  # Now includes coordinates
                    "count": len(attractions)
                }
            )
            
        except PlacesAPIError as e:
            self.logger.error(f"Places API error: {str(e)}")
            return self.format_response(
                success=False,
                error=f"Unable to fetch places for {place_name}: {str(e)}"
            )
        except Exception as e:
            self.logger.error(f"Unexpected error in places agent: {str(e)}")
            return self.format_response(
                success=False,
                error=f"An error occurred while fetching places: {str(e)}"
            )
