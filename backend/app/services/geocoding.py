"""Geocoding service using Nominatim API with spell checking and caching."""

import asyncio
import httpx
from typing import Dict, Optional
from app.config import settings
from app.utils.logger import setup_logger
from app.utils.exceptions import PlaceNotFoundError, GeocodingAPIError
from app.utils.spell_checker import SpellChecker
from app.utils.cache import geocoding_cache

logger = setup_logger(__name__)

# Global variable to track last request time for rate limiting
_last_request_time: Optional[float] = None

# Initialize spell checker
spell_checker = SpellChecker()


async def get_coordinates(place_name: str, auto_correct: bool = True) -> Dict[str, any]:
    """
    Get coordinates for a place using Nominatim geocoding API.
    
    Implements rate limiting (1 request per second as per Nominatim policy).
    Includes spell checking and caching for better UX.
    
    Args:
        place_name: Name of the place to geocode
        auto_correct: Whether to auto-correct spelling (default: True)
    
    Returns:
        Dictionary with 'lat', 'lon', and optionally 'corrected_from'
    
    Raises:
        PlaceNotFoundError: If the place cannot be found
        GeocodingAPIError: If the API request fails
    """
    global _last_request_time
    
    original_name = place_name
    corrected = False
    
    # Check cache first
    cached_result = geocoding_cache.get(place_name)
    if cached_result:
        logger.info(f"Using cached coordinates for: {place_name}")
        return cached_result
    
    # Try spell correction if enabled
    if auto_correct:
        corrected_name, was_corrected = spell_checker.check_and_correct(place_name)
        if was_corrected:
            place_name = corrected_name
            corrected = True
            logger.info(f"Auto-corrected '{original_name}' to '{place_name}'")
            
            # Check cache with corrected name
            cached_result = geocoding_cache.get(place_name)
            if cached_result:
                cached_result["corrected_from"] = original_name
                return cached_result
    
    # Rate limiting: ensure at least 1 second between requests
    if _last_request_time is not None:
        elapsed = asyncio.get_event_loop().time() - _last_request_time
        if elapsed < settings.nominatim_delay:
            await asyncio.sleep(settings.nominatim_delay - elapsed)
    
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 0
    }
    
    headers = {
        "User-Agent": f"{settings.app_name}/{settings.app_version}"
    }
    
    try:
        logger.info(f"Geocoding place: {place_name}")
        async with httpx.AsyncClient(timeout=settings.api_timeout) as client:
            response = await client.get(
                settings.nominatim_url,
                params=params,
                headers=headers
            )
            response.raise_for_status()
            
            # Update last request time
            _last_request_time = asyncio.get_event_loop().time()
            
            data = response.json()
            
            if not data or len(data) == 0:
                # If corrected name didn't work, try suggestions
                if corrected:
                    suggestions = spell_checker.suggest_correction(original_name, max_suggestions=3)
                    suggestion_text = f"Did you mean: {', '.join(suggestions)}?" if suggestions else ""
                    raise PlaceNotFoundError(f"{original_name}. {suggestion_text}")
                else:
                    # Try spell correction as fallback
                    suggestions = spell_checker.suggest_correction(place_name, max_suggestions=3)
                    if suggestions:
                        suggestion_text = f"Did you mean: {', '.join(suggestions)}?"
                        raise PlaceNotFoundError(f"{place_name}. {suggestion_text}")
                    else:
                        raise PlaceNotFoundError(place_name)
            
            result = {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }
            
            if corrected:
                result["corrected_from"] = original_name
            
            # Cache the result
            geocoding_cache.set(place_name, result)
            if corrected:
                geocoding_cache.set(original_name, result)  # Also cache with original name
            
            logger.info(f"Found coordinates for {place_name}: {result}")
            return result
            
    except httpx.HTTPError as e:
        logger.error(f"Geocoding API error for {place_name}: {str(e)}")
        raise GeocodingAPIError(f"Failed to geocode {place_name}: {str(e)}")
    except (KeyError, ValueError, IndexError) as e:
        logger.error(f"Error parsing geocoding response: {str(e)}")
        raise GeocodingAPIError(f"Invalid response from geocoding API: {str(e)}")
