import os
import shutil
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
try:
    from google.cloud import bigquery
    from google.oauth2 import service_account
    BQ_AVAILABLE = True
except ImportError:
    print("Google Cloud libraries not found. Will use JSON cache.")
    BQ_AVAILABLE = False
except Exception as e:
    print(f"Error importing Google Cloud libraries: {e}")
    BQ_AVAILABLE = False

from math import radians, cos, sin, asin, sqrt

# --- Configuration ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
INTERFERENCE_RADIUS = 0.5
INTERFERENCE_STRENGTH = 1.0
GRID_RES = 100 # Lower res per stadium since we have many
OVERLAY_DIR = "map_overlays"

def get_bq_client():
    if not BQ_AVAILABLE:
        return None
    try:
        possible_keys = [
            'shhhh/service_account.json',
            '../../../shhhh/service_account.json',
            os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
        ]
        key_path = next((p for p in possible_keys if os.path.exists(p)), None)
        
        if key_path:
            credentials = service_account.Credentials.from_service_account_file(key_path)
            return bigquery.Client(credentials=credentials, project=credentials.project_id)
        else:
            return bigquery.Client()
    except Exception as e:
        print(f"Error creating BQ client: {e}")
        return None

def haversine_vectorized(lon1, lat1, lon2_array, lat2_array):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2_array, lat2_array])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return 3956 * c

def simple_hav(lo1, la1, lo2, la2):
    lo1, la1, lo2, la2 = map(radians, [lo1, la1, lo2, la2])
    dlon = lo2 - lo1; dlat = la2 - la1
    a = sin(dlat/2)**2 + cos(la1)*cos(la2)*sin(dlon/2)**2
    return 2 * asin(sqrt(a)) * 3956

def generate_all_maps():
    client = get_bq_client()
    
    df = pd.DataFrame()
    if client:
        try:
            cols = ['team_name', 'stadium_name', 'dunkin', 'starbucks']
            query = f"""SELECT {','.join(cols)} FROM `{BQ_COFFEE_TABLE}`"""
            df = client.query(query).to_dataframe()
        except Exception as e:
            print(f"BQ Query failed: {e}")
    
    # If no DF from BQ, try loading from JSON cache
    if df.empty:
        # Try local path (same dir as script)
        json_path = os.path.join(os.path.dirname(__file__), "coffee_data_cache.json")
        if not os.path.exists(json_path):
             # Try alternate path just in case
             json_path = os.path.join(PROJECT_ROOT, "posts/super_bowl/data/prep/coffee_data_cache.json")

        if os.path.exists(json_path):
            print(f"Loading data from cache: {json_path}")
            import json
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            # Convert to DataFrame with expected columns
            rows = []
            for entry in data:
                rows.append({
                    'team_name': entry['Team'],
                    'stadium_name': entry['Stadium'],
                    'dunkin': entry.get('Dunkin_Stats', {}),
                    'starbucks': entry.get('Starbucks_Stats', {})
                })
            df = pd.DataFrame(rows)
        else:
            print("No BQ data and no cache found.")
            return

    # Map Full Name to Abbrev
    TEAM_TO_ABBREV = {
        'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL', 
        'Buffalo Bills': 'BUF', 'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 
        'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE', 'Dallas Cowboys': 'DAL', 
        'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB', 
        'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX', 
        'Kansas City Chiefs': 'KC', 'Las Vegas Raiders': 'LV', 'Los Angeles Chargers': 'LAC', 
        'Los Angeles Rams': 'LA', 'Miami Dolphins': 'MIA', 'Minnesota Vikings': 'MIN', 
        'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG', 
        'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 
        'San Francisco 49ers': 'SF', 'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB', 
        'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS'
    }

    # Reverse mapping for lookups
    TEAM_TO_ABBREV_REVERSE = {v: k for k, v in TEAM_TO_ABBREV.items()}

    # Team Primary Colors (for popup styling)
    TEAM_COLORS = {
        'ARI': '#97233F', 'ATL': '#A71930', 'BAL': '#241773', 'BUF': '#00338D',
        'CAR': '#0085CA', 'CHI': '#0B162A', 'CIN': '#FB4F14', 'CLE': '#311D00',
        'DAL': '#041E42', 'DEN': '#FB4F14', 'DET': '#0076B6', 'GB': '#203731',
        'HOU': '#03202F', 'IND': '#002C5F', 'JAX': '#006778', 'KC': '#E31837',
        'LV': '#000000', 'LAC': '#0080C6', 'LA': '#003594', 'MIA': '#008E97',
        'MIN': '#4F2683', 'NE': '#002244', 'NO': '#D3BC8D', 'NYG': '#0B2265',
        'NYJ': '#125740', 'PHI': '#004C54', 'PIT': '#FFB612', 'SF': '#AA0000',
        'SEA': '#002244', 'TB': '#D50A0A', 'TEN': '#0C2340', 'WAS': '#5A1414'
    }

    # Latest PBP Stadium Names (Must match BQ stuperlatives.coffee_wars 'stadium_name' EXACTLY)
    CURRENT_STADIUM_NAMES = {
        'NE': 'Gillette Stadium',
        'CHI': 'Soldier Field',
        'DEN': 'Empower Field at Mile High',
        'SEA': 'Lumen Field',
        'PIT': 'Acrisure Stadium',
        'PHI': 'Lincoln Financial Field',
        'JAX': 'EverBank Stadium',
        'CAR': 'Bank of America Stadium',
        'MIN': 'U.S. Bank Stadium',
        'LA': 'SoFi Stadium',
        'NYG': 'MetLife Stadium',
        'HOU': 'NRG Stadium',
        'ATL': 'Mercedes-Benz Stadium',
        'LV': 'Allegiant Stadium',
        'BUF': 'Highmark Stadium',
        'CIN': 'Paycor Stadium',
        'SF': "Levi's Stadium",          # BQ Name (Not Levi's®)
        'TB': 'Raymond James Stadium',
        'TEN': 'Nissan Stadium',
        'IND': 'Lucas Oil Stadium',
        'NYJ': 'MetLife Stadium',
        'CLE': 'Cleveland Browns Stadium', # BQ Name (Not Huntington)
        'MIA': 'Hard Rock Stadium',
        'GB': 'Lambeau Field',
        'LAC': 'SoFi Stadium',
        'KC': 'GEHA Field at Arrowhead Stadium',
        'WAS': 'Commanders Field',         # BQ Name (Not Northwest)
        'NO': 'Caesars Superdome',
        'ARI': 'State Farm Stadium',
        'DET': 'Ford Field',
        'DAL': 'AT&T Stadium',
        'BAL': 'M&T Bank Stadium',
    }

    # Coordinates (Keys must match BQ Names above)
    STADIUM_COORDS = {
        "State Farm Stadium": (33.5276, -112.2626),
        "Mercedes-Benz Stadium": (33.7554, -84.4010),
        "M&T Bank Stadium": (39.2780, -76.6227),
        "Highmark Stadium": (42.7738, -78.7870),
        "Bank of America Stadium": (35.2258, -80.8528),
        "Soldier Field": (41.8623, -87.6167),
        "Paycor Stadium": (39.0955, -84.5161),
        "Cleveland Browns Stadium": (41.5061, -81.6995),
        "AT&T Stadium": (32.7478, -97.0928),
        "Empower Field at Mile High": (39.7439, -105.0201),
        "Ford Field": (42.3400, -83.0456),
        "Lambeau Field": (44.5013, -88.0622),
        "NRG Stadium": (29.6847, -95.4107),
        "Lucas Oil Stadium": (39.7601, -86.1639),
        "EverBank Stadium": (30.3239, -81.6373),
        "GEHA Field at Arrowhead Stadium": (39.0489, -94.4839),
        "SoFi Stadium": (33.9535, -118.3390),
        "Allegiant Stadium": (36.0909, -115.1833),
        "Hard Rock Stadium": (25.9580, -80.2389),
        "U.S. Bank Stadium": (44.9739, -93.2581),
        "Gillette Stadium": (42.0909, -71.2643),
        "Caesars Superdome": (29.9511, -90.0812),
        "MetLife Stadium": (40.8135, -74.0745),
        "Lincoln Financial Field": (39.9008, -75.1675),
        "Acrisure Stadium": (40.4468, -80.0158),
        "Levi's Stadium": (37.4032, -121.9698),
        "Lumen Field": (47.5952, -122.3316),
        "Raymond James Stadium": (27.9759, -82.5033),
        "Nissan Stadium": (36.1664, -86.7713),
        "Commanders Field": (38.9076, -76.8645),
    }

    # Display Overrides (BQ Name -> Modern Display Name)
    DISPLAY_OVERRIDES = {
        "Cleveland Browns Stadium": "Huntington Bank Field",
        "Levi's Stadium": "Levi's® Stadium",
        "Commanders Field": "Northwest Stadium"
    }

    # Initialize Global Map (Center of US roughly)
    # UPDATED: Focus on Super Bowl LX (Levi's Stadium)
    m = folium.Map(location=[37.4032, -121.9698], zoom_start=11, tiles='CartoDB dark_matter')
    
    # Track processed teams
    processed_teams = set()

    # Iterate Stadiums
    for idx, row in df.iterrows():
        team_full = row['team_name']
        team_abbr = TEAM_TO_ABBREV.get(team_full)
        current_stadium_bq = row['stadium_name']
        
        if not team_abbr: continue 
        
        # 1. Identify what the BQ row SHOULD be for this team
        target_bq_name = CURRENT_STADIUM_NAMES.get(team_abbr)
        if not target_bq_name: continue
        
        # 2. Strict Match: Only process if the ROW matches the TARGET
        # This prevents 'Candlestick Park' row from being processed for SF
        if current_stadium_bq != target_bq_name:
            continue
            
        # 3. Avoid duplicates (e.g. NYG processed, then find NYG again?)
        if team_full in processed_teams: continue
        
        # Coordinates
        if target_bq_name not in STADIUM_COORDS:
            print(f"Warning: No coords for {target_bq_name}")
            continue
        stadium_lat, stadium_lng = STADIUM_COORDS[target_bq_name]
        
        processed_teams.add(team_full)
        
        # Display Name
        stadium_display_name = DISPLAY_OVERRIDES.get(target_bq_name, target_bq_name)
        
        print(f"Processing {team_full} -> {target_bq_name} (Display: {stadium_display_name})...")
        
        d_locs = row['dunkin'].get('locations', []) if row['dunkin'] else []
        s_locs = row['starbucks'].get('locations', []) if row['starbucks'] else []
        if d_locs is None: d_locs = []
        if s_locs is None: s_locs = []
        
        if len(d_locs) == 0 and len(s_locs) == 0: continue
        
        # 1. Calc Masses
        d_masses = np.ones(len(d_locs))
        s_masses = np.ones(len(s_locs))
        
        if len(d_locs) > 0 and len(s_locs) > 0:
            for i, d in enumerate(d_locs):
                for j, S in enumerate(s_locs):
                    dist = simple_hav(d['lng'], d['lat'], S['lng'], S['lat'])
                    if dist < INTERFERENCE_RADIUS:
                        reduction = INTERFERENCE_STRENGTH * (1.0 - dist/INTERFERENCE_RADIUS)
                        d_masses[i] -= reduction
                        s_masses[j] -= reduction
            d_masses = np.maximum(d_masses, 0.0)
            s_masses = np.maximum(s_masses, 0.0)

        # 2. Local Grid
        # Center grid on the ACTUAL stadium coordinates
        center_lat = stadium_lat
        center_lng = stadium_lng
        
        # Determine bounds based on actual store spread + generous fade-out buffer
        # But ensure we respect the stadium center so the view is nice.
        # Actually, let's use the store spread if it's wider, but center on the stadium.
        
        # Collect store coords for sizing
        all_lats = [x['lat'] for x in d_locs] + [x['lat'] for x in s_locs]
        all_lngs = [x['lng'] for x in d_locs] + [x['lng'] for x in s_locs]
        
        # If stores are far, extend bounds.
        # If stores are close, enforce minimum bound around stadium.
        
        buffer = 0.22 # Approx 15 miles
        
        min_lat = min(min(all_lats), center_lat) - buffer
        max_lat = max(max(all_lats), center_lat) + buffer
        
        # Longitude correction
        lng_buffer = buffer / np.cos(np.radians(center_lat))
        min_lng = min(min(all_lngs), center_lng) - lng_buffer
        max_lng = max(max(all_lngs), center_lng) + lng_buffer
        
        lats = np.linspace(min_lat, max_lat, GRID_RES)
        lngs = np.linspace(min_lng, max_lng, GRID_RES)
        lng_mesh, lat_mesh = np.meshgrid(lngs, lats)
        
        # 3. Field Calc
        d_field = np.zeros(lng_mesh.shape)
        s_field = np.zeros(lng_mesh.shape)
        
        for i, loc in enumerate(d_locs):
            if d_masses[i] > 0:
                dist = haversine_vectorized(loc['lng'], loc['lat'], lng_mesh, lat_mesh)
                d_field += d_masses[i] * np.exp(-0.5 * dist)
                
        for i, loc in enumerate(s_locs):
            if s_masses[i] > 0:
                dist = haversine_vectorized(loc['lng'], loc['lat'], lng_mesh, lat_mesh)
                s_field += s_masses[i] * np.exp(-0.5 * dist)
        
        # 4. Net Gravity Coloring (Stark Contrast)
        # Net Gravity defined as sum(D * e^-0.5d) - sum(S * e^-0.5d)
        net_field = d_field - s_field
        
        # Normalize
        limit = max(np.abs(np.min(net_field)), np.abs(np.max(net_field)))
        if limit == 0: limit = 1
        
        # Create RGBA array
        rgba = np.zeros((GRID_RES, GRID_RES, 4))
        
        # Mask for positive (Dunkin)
        pos_mask = net_field > 0
        strength = np.abs(net_field) / limit
        
        # Dunkin Orange: #FF671F -> (1.0, 0.4, 0.12)
        rgba[pos_mask, 0] = 1.0
        rgba[pos_mask, 1] = 0.4
        rgba[pos_mask, 2] = 0.12
        rgba[pos_mask, 3] = strength[pos_mask] * 1.0 # Max Stark Opacity
        
        # Starbucks Green: #00704A -> (0.0, 0.44, 0.29)
        neg_mask = net_field < 0
        rgba[neg_mask, 0] = 0.0
        rgba[neg_mask, 1] = 0.44
        rgba[neg_mask, 2] = 0.29
        rgba[neg_mask, 3] = strength[neg_mask] * 1.0 # Max Stark Opacity
        
        # Flip for Map
        rgba = np.flipud(rgba)
        
        # Save Overlay
        if not os.path.exists(OVERLAY_DIR):
            os.makedirs(OVERLAY_DIR)
        
        safe_name = "".join(x for x in team_full if x.isalnum()) + "_" + "".join(x for x in stadium_display_name if x.isalnum())
        img_name = f"{OVERLAY_DIR}/{safe_name}.png"
        plt.imsave(img_name, rgba)
        
        # Add to Map
        folium.raster_layers.ImageOverlay(
            image=img_name,
            bounds=[[min_lat, min_lng], [max_lat, max_lng]],
            opacity=0.9,
            interactive=True,
            cross_origin=False,
            zindex=1
        ).add_to(m)
        
        # Store Markers (Detailed)
        # Only plot if significant mass
        for i, loc in enumerate(d_locs):
            if d_masses[i] > 0.1: # Threshold to reduce clutter
                folium.CircleMarker(
                    [loc['lat'], loc['lng']], radius=3, color='gray', weight=0.5, fill=True, fill_color='#FF671F', fill_opacity=1.0
                ).add_to(m)
                
        for i, loc in enumerate(s_locs):
            if s_masses[i] > 0.1:
                folium.CircleMarker(
                    [loc['lat'], loc['lng']], radius=3, color='gray', weight=0.5, fill=True, fill_color='#00704A', fill_opacity=1.0
                ).add_to(m)
        
        
        # Calculate Net Gravity at Stadium Location
        # Sum all store contributions at the stadium coordinates
        stadium_d_gravity = 0
        stadium_s_gravity = 0
        
        for i, loc in enumerate(d_locs):
            if d_masses[i] > 0:
                dist = simple_hav(loc['lng'], loc['lat'], center_lng, center_lat)
                stadium_d_gravity += d_masses[i] * np.exp(-0.5 * dist)
        
        for i, loc in enumerate(s_locs):
            if s_masses[i] > 0:
                dist = simple_hav(loc['lng'], loc['lat'], center_lng, center_lat)
                stadium_s_gravity += s_masses[i] * np.exp(-0.5 * dist)
        
        net_gravity = stadium_d_gravity - stadium_s_gravity
        
        # Determine winner (no ties - always pick the higher side)
        if net_gravity >= 0:
            winner = "Dunkin'"
            winner_color = "#FF671F"
            winner_logo = "logos/dunkin.png"
        else:
            winner = "Starbucks"
            winner_color = "#00704A"
            winner_logo = "logos/starbucks.png"
        
        # Coffee chain logos for the breakdown
        dunkin_logo = "logos/dunkin.png"
        starbucks_logo = "logos/starbucks.png"
        
        # Marker with Team Logo(s)
        # ESPN logo URL format: https://a.espncdn.com/i/teamlogos/nfl/500/{team_abbr}.png
        
        # For teams sharing a stadium (NYG/NYJ, LA/LAC), place logos side-by-side
        teams_at_stadium = [t for t, s in CURRENT_STADIUM_NAMES.items() if s == target_bq_name]
        
        if len(teams_at_stadium) > 1:
            # Multiple teams - offset logos horizontally
            # Offset by ~0.002 degrees lng (~200m at mid-latitudes)
            offset = 0.002
            num_teams = len(teams_at_stadium)
            
            # Center the group of logos
            start_offset = -offset * (num_teams - 1) / 2
            
            for idx, team_abbr_shared in enumerate(teams_at_stadium):
                team_full_shared = TEAM_TO_ABBREV_REVERSE.get(team_abbr_shared, team_abbr_shared)
                logo_url = f"https://a.espncdn.com/i/teamlogos/nfl/500/{team_abbr_shared}.png"
                offset_lng = center_lng + start_offset + (idx * offset)
                team_color = TEAM_COLORS.get(team_abbr_shared, '#1e3c72')
                
                # Create combined team name for shared stadiums
                if len(teams_at_stadium) > 1:
                    all_team_names = [TEAM_TO_ABBREV_REVERSE.get(t, t) for t in teams_at_stadium]
                    team_name_display = " / ".join(all_team_names)
                else:
                    team_name_display = team_full_shared
                
                # Styled popup
                abs_gravity = abs(net_gravity)
                popup_html = f"""
                <div style="font-family: 'Arial', sans-serif; min-width: 220px;">
                    <div style="background: linear-gradient(135deg, {team_color} 0%, {team_color}dd 100%); 
                                color: white; padding: 12px; margin: -10px -10px 10px -10px; 
                                border-radius: 4px 4px 0 0; text-align: center;">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 4px;">{stadium_display_name}</div>
                        <div style="font-size: 12px; opacity: 0.9;">{team_name_display}</div>
                    </div>
                    <div style="padding: 8px 4px;">
                        <div style="margin-bottom: 12px; text-align: center; padding: 10px; background: #f5f5f5; border-radius: 4px;">
                            <div style="font-weight: bold; font-size: 12px; color: #666; margin-bottom: 4px;">Net Gravity</div>
                            <div style="font-size: 22px; font-weight: bold; color: {winner_color};">
                                +{abs_gravity:.2f}
                                <img src="{winner_logo}" style="height: 24px; vertical-align: middle; margin-left: 8px;">
                            </div>
                        </div>
                        <div style="font-size: 13px; color: #666;">
                            <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px; background: #fff3e6; border-radius: 3px;">
                                <img src="{dunkin_logo}" style="height: 18px; margin-right: 6px;">
                                <span style="margin-left: auto; font-weight: bold; color: #FF671F;">{stadium_d_gravity:.2f}</span>
                            </div>
                            <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px; background: #e6f5f0; border-radius: 3px;">
                                <img src="{starbucks_logo}" style="height: 18px; margin-right: 6px;">
                                <span style="margin-left: auto; font-weight: bold; color: #00704A;">{stadium_s_gravity:.2f}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """
                
                folium.Marker(
                    location=[center_lat, offset_lng],
                    popup=folium.Popup(popup_html, max_width=250),
                    icon=folium.CustomIcon(logo_url, icon_size=(30, 30))
                ).add_to(m)
        else:
            # Single team
            logo_url = f"https://a.espncdn.com/i/teamlogos/nfl/500/{team_abbr}.png"
            team_color = TEAM_COLORS.get(team_abbr, '#1e3c72')
            
            # Styled popup
            abs_gravity = abs(net_gravity)
            popup_html = f"""
            <div style="font-family: 'Arial', sans-serif; min-width: 220px;">
                <div style="background: linear-gradient(135deg, {team_color} 0%, {team_color}dd 100%); 
                            color: white; padding: 12px; margin: -10px -10px 10px -10px; 
                            border-radius: 4px 4px 0 0; text-align: center;">
                    <div style="font-size: 18px; font-weight: bold; margin-bottom: 4px;">{stadium_display_name}</div>
                    <div style="font-size: 12px; opacity: 0.9;">{team_full}</div>
                </div>
                <div style="padding: 8px 4px;">
                    <div style="margin-bottom: 12px; text-align: center; padding: 10px; background: #f5f5f5; border-radius: 4px;">
                        <div style="font-weight: bold; font-size: 12px; color: #666; margin-bottom: 4px;">Net Gravity</div>
                        <div style="font-size: 22px; font-weight: bold; color: {winner_color};">
                            +{abs_gravity:.2f}
                            <img src="{winner_logo}" style="height: 24px; vertical-align: middle; margin-left: 8px;">
                        </div>
                    </div>
                    <div style="font-size: 13px; color: #666;">
                        <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px; background: #fff3e6; border-radius: 3px;">
                            <img src="{dunkin_logo}" style="height: 18px; margin-right: 6px;">
                            <span style="margin-left: auto; font-weight: bold; color: #FF671F;">{stadium_d_gravity:.2f}</span>
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px; background: #e6f5f0; border-radius: 3px;">
                            <img src="{starbucks_logo}" style="height: 18px; margin-right: 6px;">
                            <span style="margin-left: auto; font-weight: bold; color: #00704A;">{stadium_s_gravity:.2f}</span>
                        </div>
                    </div>
                </div>
            </div>
            """
            
            folium.Marker(
                location=[center_lat, center_lng],
                popup=folium.Popup(popup_html, max_width=250, show=(target_bq_name == "Levi's Stadium")),
                icon=folium.CustomIcon(logo_url, icon_size=(30, 30))
            ).add_to(m)

    # ADD LEGEND
    legend_html = '''
    <div style="position: fixed; 
         bottom: 30px; right: 30px; width: 210px; height: 160px; 
         border: 1px solid #ddd; z-index:9999; font-size:13px;
         background-color: white; opacity: 0.95;
         border-radius: 8px; padding: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); font-family: sans-serif;">
         <div style="font-weight: bold; margin-bottom: 10px; font-size: 15px; border-bottom: 1px solid #eee; padding-bottom: 5px;">Coffee Gravity Legend</div>
         
         <div style="margin-bottom: 6px;">
            <div style="background:#FF671F; width:8px; height:8px; display: inline-block; vertical-align: middle; margin-right: 8px; border-radius: 50%;"></div>
            <span style="vertical-align: middle;">Dunkin' Location</span>
         </div>
         <div style="margin-bottom: 10px;">
            <div style="background:#00704A; width:8px; height:8px; display: inline-block; vertical-align: middle; margin-right: 8px; border-radius: 50%;"></div>
            <span style="vertical-align: middle;">Starbucks Location</span>
         </div>

         <div style="margin-bottom: 6px;">
            <div style="background:radial-gradient(circle, rgba(255, 103, 31, 0.9) 0%, rgba(255, 103, 31, 0.4) 100%); width:20px; height:20px; display: inline-block; vertical-align: middle; margin-right: 8px; border-radius: 50%;"></div>
            <span style="vertical-align: middle;">Net Dunkin' Force Field</span>
         </div>
         <div style="margin-bottom: 10px;">
            <div style="background:radial-gradient(circle, rgba(0, 112, 74, 0.9) 0%, rgba(0, 112, 74, 0.4) 100%); width:20px; height:20px; display: inline-block; vertical-align: middle; margin-right: 8px; border-radius: 50%;"></div>
            <span style="vertical-align: middle;">Net Starbucks Force Field</span>
         </div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save directly to assets folder to avoid duplication
    # Script is in data/prep/, assets is in ../../assets/
    output_dir = os.path.join(PROJECT_ROOT, "posts/super_bowl/assets")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "coffee_force_field_map_all.html")
    m.save(output_path)
    print(f"All-Stadium Map saved to {output_path}")

if __name__ == "__main__":
    generate_all_maps()
