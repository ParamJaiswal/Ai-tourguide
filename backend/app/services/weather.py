"""Weather service using Open-Meteo API."""

import httpx
from typing import Dict
from app.config import settings
from app.utils.logger import setup_logger
from app.utils.exceptions import WeatherAPIError

logger = setup_logger(__name__)


async def get_current_weather(lat: float, lon: float) -> Dict[str, any]:
    """
    Get current weather for coordinates using Open-Meteo API.
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        Dictionary with weather information including:
        - temperature: Current temperature in Celsius
        - precipitation_probability: Chance of rain as percentage
    
    Raises:
        WeatherAPIError: If the API request fails
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation",
        "hourly": "precipitation_probability",
        "timezone": "auto",
        "forecast_days": 1
    }
    
    try:
        logger.info(f"Fetching weather for coordinates: ({lat}, {lon})")
        async with httpx.AsyncClient(timeout=settings.api_timeout) as client:
            response = await client.get(
                settings.openmeteo_url,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract current weather data
            current = data.get("current", {})
            hourly = data.get("hourly", {})
            
            temperature = current.get("temperature_2m")
            
            # Get average precipitation probability from hourly forecast
            precip_probs = hourly.get("precipitation_probability", [])
            avg_precip_prob = sum(precip_probs) / len(precip_probs) if precip_probs else 0
            
            result = {
                "temperature": round(temperature, 1) if temperature is not None else None,
                "precipitation_probability": round(avg_precip_prob)
            }
            
            logger.info(f"Weather data retrieved: {result}")
            return result
            
    except httpx.HTTPError as e:
        logger.error(f"Weather API error: {str(e)}")
        raise WeatherAPIError(f"Failed to fetch weather data: {str(e)}")
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Error parsing weather response: {str(e)}")
        raise WeatherAPIError(f"Invalid response from weather API: {str(e)}")
