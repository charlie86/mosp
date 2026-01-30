import json
import os
import time
import shutil
from playwright.sync_api import sync_playwright

# Configuration
DATA_FILE = "prep/coffee_data_cache.json"
MAP_FILE = "coffee_force_field_map_all.html"
TOOLTIP_DIR = "screenshots/tooltips"
ZOOM_LEVEL = 15

# Whitelist of the newest stadium for each team
TARGET_STADIUMS = {
    "Arizona Cardinals": "State Farm Stadium",
    "Atlanta Falcons": "Mercedes-Benz Stadium",
    "Baltimore Ravens": "M&T Bank Stadium",
    "Buffalo Bills": "Highmark Stadium",
    "Carolina Panthers": "Bank of America Stadium",
    "Chicago Bears": "Soldier Field",
    "Cincinnati Bengals": "Paycor Stadium",
    "Cleveland Browns": "Cleveland Browns Stadium",
    "Dallas Cowboys": "AT&T Stadium",
    "Denver Broncos": "Empower Field at Mile High",
    "Detroit Lions": "Ford Field",
    "Green Bay Packers": "Lambeau Field",
    "Houston Texans": "NRG Stadium",
    "Indianapolis Colts": "Lucas Oil Stadium",
    "Jacksonville Jaguars": "EverBank Stadium",
    "Kansas City Chiefs": "GEHA Field at Arrowhead Stadium",
    "Las Vegas Raiders": "Allegiant Stadium",
    "Los Angeles Chargers": "SoFi Stadium",
    "Los Angeles Rams": "SoFi Stadium",
    "Miami Dolphins": "Hard Rock Stadium",
    "Minnesota Vikings": "U.S. Bank Stadium",
    "New England Patriots": "Gillette Stadium",
    "New Orleans Saints": "Caesars Superdome",
    "New York Giants": "MetLife Stadium",
    "New York Jets": "MetLife Stadium",
    "NFL (Pro Bowl)": "Aloha Stadium",
    "Philadelphia Eagles": "Lincoln Financial Field",
    "Pittsburgh Steelers": "Acrisure Stadium",
    "San Francisco 49ers": "Levi's Stadium",
    "Seattle Seahawks": "Lumen Field",
    "Tampa Bay Buccaneers": "Raymond James Stadium",
    "Tennessee Titans": "Nissan Stadium",
    "Washington Commanders": "Commanders Field",
}

# Overrides for popup text matching where the map differs from the whitelist
POPUP_TEXT_OVERRIDES = {
    "Washington Commanders": "Northwest Stadium", # Map has new name
    "San Francisco 49ers": "Levi", # Handle trademark symbol
    "NFL (Pro Bowl)": "Aloha",
    "New York Giants": "MetLife Stadium", # Shared stadium
    "New York Jets": "MetLife Stadium",
    "Cleveland Browns": "Huntington Bank Field"
}

def capture_tooltips():
    # Clean and recreate tooltip directory
    # if os.path.exists(TOOLTIP_DIR):
    #    shutil.rmtree(TOOLTIP_DIR)
    if not os.path.exists(TOOLTIP_DIR):
        os.makedirs(TOOLTIP_DIR)

    # Load stadium data
    with open(DATA_FILE, 'r') as f:
        stadiums = json.load(f)

    # Absolute path to the map file for Playwright
    map_path = os.path.abspath(MAP_FILE)
    map_url = f"file://{map_path}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Larger viewport to ensure popup fits comfortably
        page = browser.new_page(viewport={'width': 1000, 'height': 800})
        
        print(f"Loading map: {map_url}")
        page.goto(map_url)
        time.sleep(3) # Initial load wait

        processed_count = 0
        
        for stadium_info in stadiums:
            team = stadium_info['Team']
            stadium = stadium_info['Stadium']
            
            # Filter
            if team not in TARGET_STADIUMS or TARGET_STADIUMS[team] != stadium:
                continue

            filename = f"{team.replace(' ', '_')}_{stadium.replace(' ', '_')}_Tooltip.png"
            filepath = os.path.join(TOOLTIP_DIR, filename)
            if os.path.exists(filepath):
                print(f"Skipping existing: {filename}")
                continue

            lat = stadium_info['Lat']
            lng = stadium_info['Lng']
            
            print(f"Processing Tooltip: {team} - {stadium}")
            
            # 1. Trigger the popup via JS
            found = page.evaluate(f"""
                (function() {{
                    var map = null;
                    for(var key in window) {{
                        if (window[key] instanceof L.Map) {{
                            map = window[key];
                            break;
                        }}
                    }}
                    if (!map) return false;

                    // Close any existing popups to clean up
                    map.closePopup();

                    var targetLat = {lat};
                    var targetLng = {lng};
                    var found = false;
                    
                    map.eachLayer(function(layer) {{
                        // Look for L.Marker (not CircleMarker) near coordinates
                        if (layer instanceof L.Marker && !(layer instanceof L.CircleMarker)) {{
                             var latLng = layer.getLatLng();
                             // Increased tolerance to 0.01 to handle slight offsets (approx 1km)
                             if (Math.abs(latLng.lat - targetLat) < 0.01 && Math.abs(latLng.lng - targetLng) < 0.01) {{
                                map.setView(latLng, {ZOOM_LEVEL});
                                layer.openPopup();
                                found = true;
                             }}
                        }}
                    }});
                    return found;
                }})();
            """)

            if not found:
                print(f"Warning: Marker not found for {team} - {stadium}")
                continue

            # 2. Wait for popup to be visible using specific text
            try:
                # Determine search text
                search_text = POPUP_TEXT_OVERRIDES.get(team, stadium)
                
                popup_locator = page.locator(".leaflet-popup").filter(has_text=search_text)
                
                if popup_locator.count() > 1:
                     popup_locator = popup_locator.first

                popup_locator.wait_for(state="visible", timeout=5000)
                
                time.sleep(0.5)

                # 3. Screenshot just the popup
                filename = f"{team.replace(' ', '_')}_{stadium.replace(' ', '_')}_Tooltip.png"
                filepath = os.path.join(TOOLTIP_DIR, filename)
                
                popup_locator.screenshot(path=filepath)
                print(f"Captured: {filename}")
                processed_count += 1
                
            except Exception as e:
                print(f"Error capturing tooltip for {team}: {e}")

        print(f"Done. Processed {processed_count} tooltips.")
        browser.close()

if __name__ == "__main__":
    capture_tooltips()
