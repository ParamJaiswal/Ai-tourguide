"""Weather agent for handling weather-related queries."""

from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.services.weather import get_current_weather
from app.utils.exceptions import WeatherAPIError


class WeatherAgent(BaseAgent):
    """Agent specialized in weather information."""
    
    def __init__(self):
        super().__init__("weather")
    
    async def process(self, lat: float, lon: float, place_name: str) -> Dict[str, Any]:
        """
        Get weather information for coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            place_name: Name of the place (for response formatting)
        
        Returns:
            Formatted weather response
        """
        try:
            self.logger.info(f"Processing weather request for {place_name}")
            
            weather_data = await get_current_weather(lat, lon)
            
            # Format natural language response with tourist-friendly context
            temperature = weather_data.get("temperature")
            precip_prob = weather_data.get("precipitation_probability")
            
            if temperature is not None:
                # Add weather emoji based on conditions
                if temperature > 30:
                    weather_emoji = "🌞"
                    condition = "hot"
                elif temperature > 20:
                    weather_emoji = "☀️"
                    condition = "pleasant"
                elif temperature > 10:
                    weather_emoji = "🌤️"
                    condition = "mild"
                else:
                    weather_emoji = "🌥️"
                    condition = "cool"
                
                response_text = f"{weather_emoji} The weather in {place_name} is {condition} - currently {temperature}°C"
                
                if precip_prob is not None and precip_prob > 0:
                    if precip_prob > 70:
                        response_text += f" with a high chance ({precip_prob}%) of rain. 🌧️ Don't forget your umbrella!"
                    elif precip_prob > 40:
                        response_text += f" with a moderate chance ({precip_prob}%) of rain. ☔ Consider bringing an umbrella."
                    else:
                        response_text += f" with a slight chance ({precip_prob}%) of rain."
                else:
                    response_text += ". ✨ Perfect weather for sightseeing!"
                
                # Add clothing suggestion
                if temperature > 25:
                    response_text += "\n💡 Pack light, breathable clothing."
                elif temperature > 15:
                    response_text += "\n💡 A light jacket should be perfect."
                elif temperature > 5:
                    response_text += "\n💡 Bring a warm jacket."
                else:
                    response_text += "\n💡 Bundle up! It's quite cold."
            else:
                response_text = f"Weather information for {place_name} is currently unavailable."
            
            return self.format_response(
                success=True,
                data={
                    "text": response_text,
                    "temperature": temperature,
                    "precipitation_probability": precip_prob
                }
            )
            
        except WeatherAPIError as e:
            self.logger.error(f"Weather API error: {str(e)}")
            return self.format_response(
                success=False,
                error=f"Unable to fetch weather for {place_name}: {str(e)}"
            )
        except Exception as e:
            self.logger.error(f"Unexpected error in weather agent: {str(e)}")
            return self.format_response(
                success=False,
                error=f"An error occurred while fetching weather: {str(e)}"
            )
