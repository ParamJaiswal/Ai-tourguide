"""Map visualization service using Folium."""

import folium
from folium import plugins
from typing import List, Dict, Optional
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def create_city_map(
    city_name: str,
    city_lat: float,
    city_lon: float,
    places: List[Dict],
    weather_info: Optional[Dict] = None
) -> str:
    """
    Create an interactive map with tourist attractions marked.
    
    Args:
        city_name: Name of the city
        city_lat: City center latitude
        city_lon: City center longitude
        places: List of places with name, lat, lon, type
        weather_info: Optional weather information dict with temp and precipitation
    
    Returns:
        HTML string of the interactive map
    """
    logger.info(f"Creating map for {city_name} with {len(places)} places")
    
    # Create base map centered on the city
    m = folium.Map(
        location=[city_lat, city_lon],
        zoom_start=12,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add city marker with popup
    city_popup_html = f"""
    <div style="font-family: Arial, sans-serif; min-width: 200px;">
        <h3 style="color: #2c3e50; margin: 0 0 10px 0;">{city_name}</h3>
        <p style="margin: 5px 0;"><b>📍 City Center</b></p>
    """
    
    if weather_info:
        city_popup_html += f"""
        <hr style="margin: 10px 0;">
        <p style="margin: 5px 0;"><b>🌡️ Temperature:</b> {weather_info.get('temp', 'N/A')}°C</p>
        <p style="margin: 5px 0;"><b>🌧️ Rain Chance:</b> {weather_info.get('precipitation', 'N/A')}%</p>
        """
    
    city_popup_html += "</div>"
    
    folium.Marker(
        location=[city_lat, city_lon],
        popup=folium.Popup(city_popup_html, max_width=300),
        tooltip=f"{city_name} (City Center)",
        icon=folium.Icon(color='red', icon='home', prefix='fa')
    ).add_to(m)
    
    # Define colors for different place types
    type_colors = {
        'museum': 'purple',
        'attraction': 'blue',
        'monument': 'darkblue',
        'castle': 'darkred',
        'park': 'green',
        'viewpoint': 'orange',
        'theme_park': 'pink'
    }
    
    # Define icons for different place types
    type_icons = {
        'museum': 'university',
        'attraction': 'star',
        'monument': 'monument',
        'castle': 'fort-awesome',
        'park': 'tree',
        'viewpoint': 'eye',
        'theme_park': 'ticket'
    }
    
    # Add markers for each tourist attraction
    for idx, place in enumerate(places, 1):
        place_type = place.get('type', 'attraction')
        color = type_colors.get(place_type, 'blue')
        icon = type_icons.get(place_type, 'star')
        
        # Create detailed popup
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 180px;">
            <h4 style="color: #2c3e50; margin: 0 0 8px 0;">{place['name']}</h4>
            <p style="margin: 5px 0; color: #7f8c8d;"><b>Type:</b> {place_type.title()}</p>
            <p style="margin: 5px 0; color: #7f8c8d;"><b>Location:</b> {place['lat']:.4f}, {place['lon']:.4f}</p>
            <p style="margin: 8px 0 0 0; font-size: 12px; color: #95a5a6;">#{idx} on the list</p>
        </div>
        """
        
        folium.Marker(
            location=[place['lat'], place['lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"#{idx}: {place['name']}",
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(m)
        
        # Draw line from city center to attraction
        folium.PolyLine(
            locations=[[city_lat, city_lon], [place['lat'], place['lon']]],
            color='gray',
            weight=1,
            opacity=0.3,
            dash_array='5'
        ).add_to(m)
    
    # Add a circle showing the search radius (10km)
    folium.Circle(
        location=[city_lat, city_lon],
        radius=10000,  # 10km in meters
        color='lightblue',
        fill=True,
        fillColor='lightblue',
        fillOpacity=0.1,
        popup='Search area (10km radius)'
    ).add_to(m)
    
    # Add fullscreen button
    plugins.Fullscreen(
        position='topright',
        title='Fullscreen',
        title_cancel='Exit fullscreen',
        force_separate_button=True
    ).add_to(m)
    
    # Add measure control for distances
    plugins.MeasureControl(
        position='topleft',
        primary_length_unit='kilometers',
        secondary_length_unit='miles'
    ).add_to(m)
    
    # Add legend
    legend_html = f"""
    <div style="position: fixed; 
                bottom: 50px; right: 50px; 
                width: 250px; 
                background-color: white; 
                border: 2px solid grey; 
                border-radius: 5px;
                z-index: 9999; 
                font-size: 14px;
                padding: 10px;
                box-shadow: 0 0 15px rgba(0,0,0,0.2);">
        <h4 style="margin: 0 0 10px 0; color: #2c3e50;">🗺️ Map Legend</h4>
        <p style="margin: 5px 0;"><i class="fa fa-home" style="color: red;"></i> City Center</p>
        <p style="margin: 5px 0;"><i class="fa fa-star" style="color: blue;"></i> Tourist Attraction</p>
        <p style="margin: 5px 0;"><i class="fa fa-university" style="color: purple;"></i> Museum</p>
        <p style="margin: 5px 0;"><i class="fa fa-tree" style="color: green;"></i> Park</p>
        <p style="margin: 5px 0;"><i class="fa fa-monument" style="color: darkblue;"></i> Monument</p>
        <hr style="margin: 10px 0;">
        <p style="margin: 5px 0; font-size: 12px; color: #7f8c8d;">
            <b>{len(places)}</b> places found<br>
            Click markers for details
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add custom CSS for better styling
    custom_css = """
    <style>
        .leaflet-popup-content-wrapper {
            border-radius: 8px;
        }
        .leaflet-popup-content h3, .leaflet-popup-content h4 {
            margin-top: 0;
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))
    
    # Generate HTML
    html_map = m._repr_html_()
    
    logger.info(f"Map created successfully for {city_name}")
    return html_map


def create_enhanced_map_html(
    city_name: str,
    city_lat: float,
    city_lon: float,
    places: List[Dict],
    weather_info: Optional[Dict] = None
) -> str:
    """
    Create a complete HTML page with embedded map and information sidebar.
    
    Args:
        city_name: Name of the city
        city_lat: City center latitude
        city_lon: City center longitude
        places: List of places with name, lat, lon, type
        weather_info: Optional weather information
    
    Returns:
        Complete HTML page as string
    """
    # Generate the map
    map_html = create_city_map(city_name, city_lat, city_lon, places, weather_info)
    
    # Create places list HTML
    places_list_html = ""
    for idx, place in enumerate(places, 1):
        places_list_html += f"""
        <div class="place-item">
            <div class="place-number">{idx}</div>
            <div class="place-info">
                <div class="place-name">{place['name']}</div>
                <div class="place-type">{place.get('type', 'attraction').title()}</div>
            </div>
        </div>
        """
    
    # Weather section HTML
    weather_html = ""
    if weather_info:
        weather_html = f"""
        <div class="info-section">
            <h3>🌤️ Current Weather</h3>
            <div class="weather-info">
                <div class="weather-item">
                    <span class="weather-label">Temperature</span>
                    <span class="weather-value">{weather_info.get('temp', 'N/A')}°C</span>
                </div>
                <div class="weather-item">
                    <span class="weather-label">Rain Chance</span>
                    <span class="weather-value">{weather_info.get('precipitation', 'N/A')}%</span>
                </div>
            </div>
        </div>
        """
    
    # Complete HTML page
    complete_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{city_name} - Tourist Map</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                height: 100vh;
                overflow: hidden;
            }}
            
            .sidebar {{
                width: 350px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                overflow-y: auto;
                box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            }}
            
            .sidebar h1 {{
                font-size: 28px;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            
            .sidebar h2 {{
                font-size: 16px;
                font-weight: 300;
                margin-bottom: 20px;
                opacity: 0.9;
            }}
            
            .info-section {{
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
            }}
            
            .info-section h3 {{
                font-size: 18px;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .weather-info {{
                display: flex;
                flex-direction: column;
                gap: 10px;
            }}
            
            .weather-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px;
                background: rgba(255,255,255,0.1);
                border-radius: 5px;
            }}
            
            .weather-label {{
                font-size: 14px;
                opacity: 0.9;
            }}
            
            .weather-value {{
                font-size: 18px;
                font-weight: bold;
            }}
            
            .places-list {{
                display: flex;
                flex-direction: column;
                gap: 10px;
            }}
            
            .place-item {{
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 12px;
                display: flex;
                align-items: center;
                gap: 12px;
                transition: all 0.3s ease;
                cursor: pointer;
            }}
            
            .place-item:hover {{
                background: rgba(255,255,255,0.2);
                transform: translateX(5px);
            }}
            
            .place-number {{
                width: 30px;
                height: 30px;
                background: white;
                color: #667eea;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }}
            
            .place-info {{
                flex: 1;
            }}
            
            .place-name {{
                font-size: 15px;
                font-weight: 500;
                margin-bottom: 4px;
            }}
            
            .place-type {{
                font-size: 12px;
                opacity: 0.8;
            }}
            
            .map-container {{
                flex: 1;
                position: relative;
            }}
            
            .map-container iframe {{
                width: 100%;
                height: 100%;
                border: none;
            }}
            
            .stats {{
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }}
            
            .stat-box {{
                flex: 1;
                background: rgba(255,255,255,0.1);
                padding: 10px;
                border-radius: 8px;
                text-align: center;
            }}
            
            .stat-number {{
                font-size: 24px;
                font-weight: bold;
                display: block;
            }}
            
            .stat-label {{
                font-size: 12px;
                opacity: 0.8;
                display: block;
                margin-top: 5px;
            }}
            
            @media (max-width: 768px) {{
                body {{
                    flex-direction: column;
                }}
                
                .sidebar {{
                    width: 100%;
                    max-height: 40vh;
                }}
                
                .map-container {{
                    height: 60vh;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h1>📍 {city_name}</h1>
            <h2>Tourist Attractions Map</h2>
            
            <div class="stats">
                <div class="stat-box">
                    <span class="stat-number">{len(places)}</span>
                    <span class="stat-label">Places</span>
                </div>
                <div class="stat-box">
                    <span class="stat-number">10km</span>
                    <span class="stat-label">Radius</span>
                </div>
            </div>
            
            {weather_html}
            
            <div class="info-section">
                <h3>🏛️ Top Attractions</h3>
                <div class="places-list">
                    {places_list_html}
                </div>
            </div>
            
            <div class="info-section" style="background: rgba(255,255,255,0.05);">
                <p style="font-size: 12px; opacity: 0.8; line-height: 1.6;">
                    💡 <b>Tip:</b> Click on markers for more details. Use the fullscreen button and measure tool on the map for better exploration.
                </p>
            </div>
        </div>
        
        <div class="map-container">
            {map_html}
        </div>
    </body>
    </html>
    """
    
    return complete_html
