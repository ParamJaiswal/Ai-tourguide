"""Places service using Overpass API."""

import httpx
from typing import List, Dict
from app.config import settings
from app.utils.logger import setup_logger
from app.utils.exceptions import PlacesAPIError

logger = setup_logger(__name__)


def _is_english_text(text: str) -> bool:
    """
    Check if text is primarily English (uses Latin characters).
    
    Args:
        text: Text to check
    
    Returns:
        True if text appears to be English
    """
    if not text:
        return False
    
    # Count Latin characters vs others
    latin_chars = sum(1 for c in text if ord(c) < 128 and c.isalpha())
    total_chars = sum(1 for c in text if c.isalpha())
    
    if total_chars == 0:
        return False
    
    # More lenient: at least 50% should be Latin characters (for mixed names)
    # This allows Indian place names in English script
    return (latin_chars / total_chars) >= 0.5


def _get_english_name(tags: Dict) -> str:
    """
    Extract English name from OSM tags.
    
    Tries in order:
    1. name:en (English name)
    2. name (default name - often already in English for India)
    3. int_name (international name)
    4. official_name (official name)
    
    Args:
        tags: OSM element tags
    
    Returns:
        English name or None
    """
    # Priority 1: Explicit English name
    if "name:en" in tags and tags["name:en"]:
        return tags["name:en"]
    
    # Priority 2: Default name (often already in English for India and many countries)
    if "name" in tags and tags["name"]:
        return tags["name"]
    
    # Priority 3: International name
    if "int_name" in tags and tags["int_name"]:
        return tags["int_name"]
    
    # Priority 4: Official name
    if "official_name" in tags and tags["official_name"]:
        return tags["official_name"]
    
    return None


async def get_tourist_attractions(lat: float, lon: float, radius: int = 10000) -> List[Dict]:
    """
    Get tourist attractions near coordinates using Overpass API.
    Returns place names and coordinates in English.
    
    Args:
        lat: Latitude
        lon: Longitude
        radius: Search radius in meters (default: 10km)
    
    Returns:
        List of up to 5 tourist attractions with name, lat, lon
    
    Raises:
        PlacesAPIError: If the API request fails
    """
    # Overpass QL query to find tourist attractions
    # Request all name tags to get English names
    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"="attraction"](around:{radius},{lat},{lon});
      node["tourism"="museum"](around:{radius},{lat},{lon});
      node["tourism"="viewpoint"](around:{radius},{lat},{lon});
      node["tourism"="theme_park"](around:{radius},{lat},{lon});
      node["historic"="monument"](around:{radius},{lat},{lon});
      node["historic"="castle"](around:{radius},{lat},{lon});
      node["leisure"="park"](around:{radius},{lat},{lon});
      way["tourism"="attraction"](around:{radius},{lat},{lon});
      way["tourism"="museum"](around:{radius},{lat},{lon});
      way["leisure"="park"](around:{radius},{lat},{lon});
      way["historic"="monument"](around:{radius},{lat},{lon});
    );
    out tags center;
    """
    
    try:
        logger.info(f"Fetching tourist attractions near ({lat}, {lon})")
        async with httpx.AsyncClient(timeout=settings.api_timeout) as client:
            response = await client.post(
                settings.overpass_url,
                data={"data": query}
            )
            response.raise_for_status()
            
            data = response.json()
            elements = data.get("elements", [])
            
            # Extract English place names with coordinates
            places = []
            seen_names = set()  # To avoid duplicates
            
            for element in elements:
                tags = element.get("tags", {})
                
                # Get English name
                name = _get_english_name(tags)
                
                if name and name not in seen_names:
                    # Filter out names with non-Latin scripts (Arabic, Chinese, etc.)
                    if _is_english_text(name):
                        # Extract coordinates
                        place_lat = element.get("lat")
                        place_lon = element.get("lon")
                        
                        # For ways, get center coordinates
                        if not place_lat and "center" in element:
                            place_lat = element["center"].get("lat")
                            place_lon = element["center"].get("lon")
                        
                        if place_lat and place_lon:
                            place_info = {
                                "name": name,
                                "lat": place_lat,
                                "lon": place_lon,
                                "type": tags.get("tourism", tags.get("historic", tags.get("leisure", "attraction")))
                            }
                            places.append(place_info)
                            seen_names.add(name)
                            logger.debug(f"Added place: {name} at ({place_lat}, {place_lon})")
                        else:
                            logger.debug(f"Skipped place without coordinates: {name}")
                    else:
                        logger.debug(f"Filtered non-Latin name: {name}")
                    
                    # Limit to 5 places
                    if len(places) >= 5:
                        break
            
            if places:
                logger.info(f"Found {len(places)} tourist attractions with Latin names")
            else:
                logger.warning(f"No tourist attractions found near ({lat}, {lon})")
            
            return places
            
    except httpx.HTTPError as e:
        logger.error(f"Places API error: {str(e)}")
        raise PlacesAPIError(f"Failed to fetch tourist attractions: {str(e)}")
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing places response: {str(e)}")
        raise PlacesAPIError(f"Invalid response from places API: {str(e)}")
