"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional


class TourismQuery(BaseModel):
    """Request model for tourism queries."""
    
    query: str = Field(
        ...,
        description="User query about a place (weather, attractions, etc.)",
        min_length=1,
        examples=["I'm going to go to Bangalore, what is the temperature there?"]
    )


class TourismResponse(BaseModel):
    """Response model for tourism queries."""
    
    success: bool = Field(
        description="Whether the query was processed successfully"
    )
    
    message: str = Field(
        description="Formatted response text"
    )
    
    place_name: Optional[str] = Field(
        default=None,
        description="Extracted place name"
    )
    
    coordinates: Optional[dict] = Field(
        default=None,
        description="Coordinates of the place (lat, lon)"
    )
    
    places: Optional[list] = Field(
        default=None,
        description="List of tourist attractions with coordinates"
    )
    
    weather: Optional[dict] = Field(
        default=None,
        description="Weather information"
    )


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    error: str = Field(
        description="Error message"
    )
    
    detail: Optional[str] = Field(
        default=None,
        description="Additional error details"
    )
