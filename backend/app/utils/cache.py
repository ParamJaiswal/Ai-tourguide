"""Cache manager for improving response times."""

from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class CacheManager:
    """Simple in-memory cache for geocoding and places results."""
    
    def __init__(self, ttl_minutes: int = 60):
        """
        Initialize cache manager.
        
        Args:
            ttl_minutes: Time-to-live for cached items in minutes
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = timedelta(minutes=ttl_minutes)
        self.logger = setup_logger(__name__)
        self.hits = 0
        self.misses = 0
    
    def _is_expired(self, timestamp: datetime) -> bool:
        """Check if a cache entry has expired."""
        return datetime.now() - timestamp > self.ttl
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        key = key.lower()  # Case-insensitive keys
        
        if key in self._cache:
            entry = self._cache[key]
            
            # Check if expired
            if self._is_expired(entry["timestamp"]):
                self.logger.debug(f"Cache expired for key: {key}")
                del self._cache[key]
                self.misses += 1
                return None
            
            self.hits += 1
            self.logger.debug(f"Cache hit for key: {key}")
            return entry["value"]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        key = key.lower()  # Case-insensitive keys
        
        self._cache[key] = {
            "value": value,
            "timestamp": datetime.now()
        }
        
        self.logger.debug(f"Cached key: {key}")
    
    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
        self.logger.info("Cache cleared")


# Global cache instances
geocoding_cache = CacheManager(ttl_minutes=1440)  # 24 hours for geocoding
places_cache = CacheManager(ttl_minutes=60)  # 1 hour for places
