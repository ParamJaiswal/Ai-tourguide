"""FastAPI main application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.models import TourismQuery, TourismResponse, ErrorResponse
from app.agents.parent_agent import ParentAgent
from app.utils.logger import setup_logger
from app.services.map_service import create_enhanced_map_html

logger = setup_logger(__name__)

# Global parent agent instance
parent_agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    global parent_agent
    
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    parent_agent = ParentAgent()
    logger.info("Parent agent initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multi-agent tourism system with weather and places information",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Multi-agent tourism system with interactive maps",
        "endpoints": {
            "query": "/api/tourism/query",
            "map": "/api/tourism/map",
            "health": "/health"
        },
        "features": [
            "Weather information",
            "Tourist attractions",
            "Spell correction",
            "Interactive maps",
            "Natural language queries"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


@app.post(
    "/api/tourism/query",
    response_model=TourismResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def tourism_query(query: TourismQuery) -> TourismResponse:
    """
    Process a tourism query using the multi-agent system.
    
    This endpoint accepts natural language queries about places and returns
    information about weather, tourist attractions, or both.
    
    Examples:
    - "I'm going to go to Bangalore, what is the temperature there?"
    - "What places can I visit in Paris?"
    - "I want to visit Tokyo, what's the weather and what can I see?"
    """
    try:
        logger.info(f"Received query: {query.query}")
        
        # Process query through parent agent
        result = await parent_agent.process(query.query)
        
        # Extract response data
        response_data = result.get("data", {})
        
        return TourismResponse(
            success=result.get("success", True),
            message=response_data.get("text", ""),
            place_name=response_data.get("place_name"),
            coordinates=response_data.get("coordinates"),
            places=response_data.get("places"),
            weather=response_data.get("weather")
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your query: {str(e)}"
        )


@app.post(
    "/api/tourism/map",
    response_class=HTMLResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def tourism_map(query: TourismQuery) -> HTMLResponse:
    """
    Generate an interactive map for a tourism query.
    
    This endpoint processes a query and returns an interactive HTML map
    with tourist attractions marked.
    
    Examples:
    - "Show me Paris"
    - "Map of Tokyo attractions"
    - "Places to visit in London"
    
    Returns:
        HTML page with interactive map
    """
    try:
        logger.info(f"Received map request: {query.query}")
        
        # Process query through parent agent
        result = await parent_agent.process(query.query)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("data", {}).get("text", "Could not process query")
            )
        
        response_data = result.get("data", {})
        place_name = response_data.get("place_name")
        coordinates = response_data.get("coordinates")
        places = response_data.get("places", [])
        weather = response_data.get("weather")
        
        if not place_name or not coordinates:
            raise HTTPException(
                status_code=400,
                detail="Could not identify location from query"
            )
        
        if not places:
            # Return a simple message if no places found
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{place_name} - No Places Found</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    }}
                    .message {{
                        text-align: center;
                        padding: 40px;
                        background: rgba(255,255,255,0.1);
                        border-radius: 10px;
                        backdrop-filter: blur(10px);
                    }}
                    h1 {{ margin-bottom: 20px; }}
                    p {{ font-size: 18px; line-height: 1.6; }}
                </style>
            </head>
            <body>
                <div class="message">
                    <h1>📍 {place_name}</h1>
                    <p>No tourist attractions found in the database for this location.</p>
                    <p>Try a major city or popular tourist destination.</p>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content)
        
        # Create the enhanced map
        map_html = create_enhanced_map_html(
            city_name=place_name,
            city_lat=coordinates['lat'],
            city_lon=coordinates['lon'],
            places=places,
            weather_info=weather
        )
        
        return HTMLResponse(content=map_html)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating map: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the map: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=str(exc)
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).model_dump()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
