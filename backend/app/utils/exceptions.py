"""Custom exceptions for the application."""


class TourismSystemError(Exception):
    """Base exception for tourism system errors."""
    pass


class PlaceNotFoundError(TourismSystemError):
    """Raised when a place cannot be found in geocoding."""
    
    def __init__(self, place_name: str):
        self.place_name = place_name
        super().__init__(f"Place not found: {place_name}")


class WeatherAPIError(TourismSystemError):
    """Raised when weather API request fails."""
    pass


class PlacesAPIError(TourismSystemError):
    """Raised when places API request fails."""
    pass


class GeocodingAPIError(TourismSystemError):
    """Raised when geocoding API request fails."""
    pass
