import json
import os
import time
import shutil
from playwright.sync_api import sync_playwright

# Configuration
DATA_FILE = "prep/coffee_data_cache.json"
MAP_FILE = "coffee_force_field_map_all.html"
SCREENSHOT_DIR = "screenshots"
ZOOM_LEVEL = 11

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

def capture_screenshots():
    # Clean and recreate screenshot directory
    if os.path.exists(SCREENSHOT_DIR):
        shutil.rmtree(SCREENSHOT_DIR)
    os.makedirs(SCREENSHOT_DIR)

    # Load stadium data
    with open(DATA_FILE, 'r') as f:
        stadiums = json.load(f)

    # Absolute path to the map file for Playwright
    map_path = os.path.abspath(MAP_FILE)
    map_url = f"file://{map_path}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 800, 'height': 600})
        
        print(f"Loading map: {map_url}")
        page.goto(map_url)
        
        # Inject CSS to hide zoom control and leaflet attribution
        page.add_style_tag(content="""
            .leaflet-control-zoom { display: none !important; }
            .leaflet-control-attribution { display: none !important; }
            .leaflet-bottom.leaflet-right { display: none !important; }
        """)
        
        # Wait for the map to stabilize
        time.sleep(2) 

        processed_count = 0
        for stadium_info in stadiums:
            team = stadium_info['Team']
            stadium = stadium_info['Stadium']
            
            # Filter: Check if this is the target stadium for the team
            if team not in TARGET_STADIUMS:
                continue
            if TARGET_STADIUMS[team] != stadium:
                continue

            lat = stadium_info['Lat']
            lng = stadium_info['Lng']
            
            print(f"Processing: {team} - {stadium}")
            
            # Javascript to find the first Leaflet map on the page and move it.
            page.evaluate(f"""
                (function() {{
                    for(var key in window) {{
                        if (window[key] instanceof L.Map) {{
                            window[key].setView([{lat}, {lng}], {ZOOM_LEVEL});
                            return;
                        }}
                    }}
                }})();
            """)
            
            # Wait for tiles to load
            time.sleep(1.5)
            
            # Take screenshot
            filename = f"{team.replace(' ', '_')}_{stadium.replace(' ', '_')}.png"
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            page.screenshot(path=filepath)
            print(f"Captured: {filename}")
            processed_count += 1

        print(f"Done. Processed {processed_count} stadiums.")
        browser.close()

if __name__ == "__main__":
    capture_screenshots()
