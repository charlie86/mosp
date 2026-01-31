import os
import sys
import json
import math
import time
import multiprocessing
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account
import googlemaps

# --- Configuration ---
RADIUS_MILES = 10
RADIUS_METERS = RADIUS_MILES * 1609.34
BQ_PROJECT = "gen-lang-client-0400686052"
BQ_TABLE = "stuperlatives.coffee_wars"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

# --- Data Sources ---

# 1. Current Stadiums
CURRENT_STADIUMS = [
    {"Team": "Arizona Cardinals", "Stadium": "State Farm Stadium", "Lat": 33.5276, "Lng": -112.2626},
    {"Team": "Atlanta Falcons", "Stadium": "Mercedes-Benz Stadium", "Lat": 33.7554, "Lng": -84.4009},
    {"Team": "Baltimore Ravens", "Stadium": "M&T Bank Stadium", "Lat": 39.2780, "Lng": -76.6227},
    {"Team": "Buffalo Bills", "Stadium": "Highmark Stadium", "Lat": 42.7738, "Lng": -78.7870},
    {"Team": "Carolina Panthers", "Stadium": "Bank of America Stadium", "Lat": 35.2258, "Lng": -80.8528},
    {"Team": "Chicago Bears", "Stadium": "Soldier Field", "Lat": 41.8623, "Lng": -87.6167},
    {"Team": "Cincinnati Bengals", "Stadium": "Paycor Stadium", "Lat": 39.0955, "Lng": -84.5161},
    {"Team": "Cleveland Browns", "Stadium": "Cleveland Browns Stadium", "Lat": 41.5061, "Lng": -81.6995},
    {"Team": "Dallas Cowboys", "Stadium": "AT&T Stadium", "Lat": 32.7473, "Lng": -97.0945},
    {"Team": "Denver Broncos", "Stadium": "Empower Field at Mile High", "Lat": 39.7439, "Lng": -105.0201},
    {"Team": "Detroit Lions", "Stadium": "Ford Field", "Lat": 42.3400, "Lng": -83.0456},
    {"Team": "Green Bay Packers", "Stadium": "Lambeau Field", "Lat": 44.5013, "Lng": -88.0622},
    {"Team": "Houston Texans", "Stadium": "NRG Stadium", "Lat": 29.6847, "Lng": -95.4107},
    {"Team": "Indianapolis Colts", "Stadium": "Lucas Oil Stadium", "Lat": 39.7601, "Lng": -86.1639},
    {"Team": "Jacksonville Jaguars", "Stadium": "EverBank Stadium", "Lat": 30.3239, "Lng": -81.6373},
    {"Team": "Kansas City Chiefs", "Stadium": "GEHA Field at Arrowhead Stadium", "Lat": 39.0489, "Lng": -94.4839},
    {"Team": "Las Vegas Raiders", "Stadium": "Allegiant Stadium", "Lat": 36.0909, "Lng": -115.1833},
    {"Team": "Los Angeles Chargers", "Stadium": "SoFi Stadium", "Lat": 33.9534, "Lng": -118.3390},
    {"Team": "Los Angeles Rams", "Stadium": "SoFi Stadium", "Lat": 33.9534, "Lng": -118.3390},
    {"Team": "Miami Dolphins", "Stadium": "Hard Rock Stadium", "Lat": 25.9580, "Lng": -80.2389},
    {"Team": "Minnesota Vikings", "Stadium": "U.S. Bank Stadium", "Lat": 44.9735, "Lng": -93.2575},
    {"Team": "New England Patriots", "Stadium": "Gillette Stadium", "Lat": 42.0909, "Lng": -71.2643},
    {"Team": "New Orleans Saints", "Stadium": "Caesars Superdome", "Lat": 29.9511, "Lng": -90.0812},
    {"Team": "New York Giants", "Stadium": "MetLife Stadium", "Lat": 40.8135, "Lng": -74.0745},
    {"Team": "New York Jets", "Stadium": "MetLife Stadium", "Lat": 40.8135, "Lng": -74.0745},
    {"Team": "Philadelphia Eagles", "Stadium": "Lincoln Financial Field", "Lat": 39.9008, "Lng": -75.1675},
    {"Team": "Pittsburgh Steelers", "Stadium": "Acrisure Stadium", "Lat": 40.4468, "Lng": -80.0158},
    {"Team": "San Francisco 49ers", "Stadium": "Levi's Stadium", "Lat": 37.4032, "Lng": -121.9698},
    {"Team": "Seattle Seahawks", "Stadium": "Lumen Field", "Lat": 47.5952, "Lng": -122.3316},
    {"Team": "Tampa Bay Buccaneers", "Stadium": "Raymond James Stadium", "Lat": 27.9759, "Lng": -82.5033},
    {"Team": "Tennessee Titans", "Stadium": "Nissan Stadium", "Lat": 36.1665, "Lng": -86.7713},
    {"Team": "Washington Commanders", "Stadium": "Commanders Field", "Lat": 38.9076, "Lng": -76.8645}
]

# 2. Historical/Renamed Stadiums (Copied from fetch_stadium_ihop_data.py)
MANUAL_STADIUM_COORDS = {
    # Renamed (Use current location)
    'Heinz Field': {'lat': 40.4468, 'lng': -80.0158, 'team': 'Pittsburgh Steelers'}, 
    'Paul Brown Stadium': {'lat': 39.0955, 'lng': -84.5161, 'team': 'Cincinnati Bengals'}, 
    'CenturyLink Field': {'lat': 47.5952, 'lng': -122.3316, 'team': 'Seattle Seahawks'}, 
    'Qwest Field': {'lat': 47.5952, 'lng': -122.3316, 'team': 'Seattle Seahawks'}, 
    'FirstEnergy Stadium': {'lat': 41.5061, 'lng': -81.6995, 'team': 'Cleveland Browns'}, 
    'TIAA Bank Field': {'lat': 30.3240, 'lng': -81.6373, 'team': 'Jacksonville Jaguars'}, 
    'EverBank Field': {'lat': 30.3240, 'lng': -81.6373, 'team': 'Jacksonville Jaguars'},
    'Jacksonville Municipal Stadium': {'lat': 30.3240, 'lng': -81.6373, 'team': 'Jacksonville Jaguars'},
    'Alltel Stadium': {'lat': 30.3240, 'lng': -81.6373, 'team': 'Jacksonville Jaguars'},
    'Georgia Dome': {'lat': 33.7577, 'lng': -84.4008, 'team': 'Atlanta Falcons'}, 
    'Sun Life Stadium': {'lat': 25.9580, 'lng': -80.2389, 'team': 'Miami Dolphins'}, 
    'Dolphin Stadium': {'lat': 25.9580, 'lng': -80.2389, 'team': 'Miami Dolphins'},
    'New Era Field': {'lat': 42.7738, 'lng': -78.7870, 'team': 'Buffalo Bills'}, 
    'Ralph Wilson Stadium': {'lat': 42.7738, 'lng': -78.7870, 'team': 'Buffalo Bills'},
    'Oakland-Alameda County Coliseum': {'lat': 37.7516, 'lng': -122.2005, 'team': 'Oakland Raiders'},
    'O.co Coliseum': {'lat': 37.7516, 'lng': -122.2005, 'team': 'Oakland Raiders'},
    'McAfee Coliseum': {'lat': 37.7516, 'lng': -122.2005, 'team': 'Oakland Raiders'},
    'Reliant Stadium': {'lat': 29.6847, 'lng': -95.4107, 'team': 'Houston Texans'}, 
    'Invesco Field at Mile High': {'lat': 39.7439, 'lng': -105.0201, 'team': 'Denver Broncos'}, 
    'Sports Authority Field at Mile High': {'lat': 39.7439, 'lng': -105.0201, 'team': 'Denver Broncos'},
    'Edward Jones Dome': {'lat': 38.6328, 'lng': -90.1885, 'team': 'St. Louis Rams'}, 
    'Louisiana Superdome': {'lat': 29.9511, 'lng': -90.0812, 'team': 'New Orleans Saints'}, 
    'Mercedes-Benz Superdome': {'lat': 29.9511, 'lng': -90.0812, 'team': 'New Orleans Saints'},
    'University of Phoenix Stadium': {'lat': 33.5276, 'lng': -112.2626, 'team': 'Arizona Cardinals'}, 
    'Cowboys Stadium': {'lat': 32.7473, 'lng': -97.0945, 'team': 'Dallas Cowboys'}, 
    'New Meadowlands Stadium': {'lat': 40.8135, 'lng': -74.0745, 'team': 'New York Giants/Jets'}, 
    'StubHub Center': {'lat': 33.8644, 'lng': -118.2611, 'team': 'Los Angeles Chargers'}, 
    'Mall of America Field': {'lat': 44.9735, 'lng': -93.2575, 'team': 'Minnesota Vikings'}, 
    'Hubert H. Humphrey Metrodome': {'lat': 44.9735, 'lng': -93.2575, 'team': 'Minnesota Vikings'},
    'TCF Bank Stadium': {'lat': 44.9765, 'lng': -93.2246, 'team': 'Minnesota Vikings'}, 
    'Rogers Centre': {'lat': 43.6414, 'lng': -79.3894, 'team': 'Buffalo Bills'}, 
    'Arrowhead Stadium': {'lat': 39.0489, 'lng': -94.4839, 'team': 'Kansas City Chiefs'}, 
    'LP Field': {'lat': 36.1665, 'lng': -86.7713, 'team': 'Tennessee Titans'}, 
    'FedExField': {'lat': 38.9076, 'lng': -76.8645, 'team': 'Washington Commanders'}, 
    'Los Angeles Memorial Coliseum': {'lat': 34.0141, 'lng': -118.2879, 'team': 'Los Angeles Rams'}, 
    'Qualcomm Stadium': {'lat': 32.7831, 'lng': -117.1196, 'team': 'San Diego Chargers'}, 
    
    # Historical / Demolished
    'Candlestick Park': {'lat': 37.7136, 'lng': -122.3862, 'team': 'San Francisco 49ers'},
    'Monster Park': {'lat': 37.7136, 'lng': -122.3862, 'team': 'San Francisco 49ers'},
    'Texas Stadium': {'lat': 32.8400, 'lng': -96.9110, 'team': 'Dallas Cowboys'},
    'Giants Stadium': {'lat': 40.8135, 'lng': -74.0745, 'team': 'New York Giants/Jets'}, 
    'RCA Dome': {'lat': 39.7639, 'lng': -86.1639, 'team': 'Indianapolis Colts'},
    'Aloha Stadium': {'lat': 21.3728, 'lng': -157.9294, 'team': 'NFL (Pro Bowl)'},
}

# --- Helper Functions ---

def get_google_maps_client():
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    key_file_path = os.path.join(PROJECT_ROOT, 'shhhh/google_maps_api.key')
    if not api_key and os.path.exists(key_file_path):
        try:
            with open(key_file_path, 'r') as f:
                api_key = f.read().strip()
        except Exception: pass

    if not api_key:
        print("Error: Google Maps API Key not found.")
        return None
    return googlemaps.Client(key=api_key)

def get_bq_client():
    try:
        possible_keys = [
            'shhhh/service_account.json',
            '../../../shhhh/service_account.json',
            os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
        ]
        key_path = next((p for p in possible_keys if os.path.exists(p)), None)
        
        if key_path:
            credentials = service_account.Credentials.from_service_account_file(key_path)
            return bigquery.Client(credentials=credentials, project=BQ_PROJECT)
        else:
            return bigquery.Client(project=BQ_PROJECT)
    except Exception as e:
        print(f"Error creating BQ client: {e}")
        return None

def haversine_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return c * 3956 # Miles

def find_all_places_nearby(gmaps, lat, lng, keyword, radius_meters):
    places = []
    next_page_token = None
    
    while True:
        try:
            params = {
                'location': (lat, lng),
                'keyword': keyword,
                'radius': radius_meters,
                'type': 'restaurant' # 'cafe' might be safer for coffee but 'restaurant'+keyword is ok
            }
            if next_page_token:
                params['page_token'] = next_page_token

            result = gmaps.places_nearby(**params)
            
            if result.get('results'):
                for place in result['results']:
                    name = place.get('name', '')
                    # Broad search confirmation
                    if keyword.lower() in name.lower() or name.lower() in keyword.lower():
                        loc = place['geometry']['location']
                        dist = haversine_distance(lat, lng, loc['lat'], loc['lng'])
                        places.append({
                            'name': name,
                            'lat': loc['lat'],
                            'lng': loc['lng'],
                            'distance_miles': round(dist, 4)
                        })
            
            next_page_token = result.get('next_page_token')
            if not next_page_token:
                break
            
            # Google Places API requires slight delay for token to become valid
            time.sleep(2) 
            
        except Exception as e:
            print(f"Error in places search: {e}")
            break
            
    return places

def process_stadium(stadium):
    # stadium is a dict
    team_name = stadium.get('Team', 'Unknown')
    std_name = stadium['Stadium']
    lat = stadium['StadiumLat']
    lng = stadium['StadiumLng']
    
    print(f"Processing {std_name}...")
    
    # Initialize separate client per process
    gmaps = get_google_maps_client()
    if not gmaps: return None
    
    # Search for Dunkin (broadly) and Starbucks
    dunkins = find_all_places_nearby(gmaps, lat, lng, "Dunkin", RADIUS_METERS)
    starbucks = find_all_places_nearby(gmaps, lat, lng, "Starbucks", RADIUS_METERS)
    
    def get_stats(places):
        if not places: return {'count_10mi': 0, 'closest_miles': 999.9, 'closest_location_name': 'None', 'locations': []}
        places_sorted = sorted(places, key=lambda x: x['distance_miles'])
        return {
            'count_10mi': len(places),
            'closest_miles': places_sorted[0]['distance_miles'],
            'closest_location_name': places_sorted[0]['name'],
            'locations': places_sorted
        }

    d_stats = get_stats(dunkins)
    s_stats = get_stats(starbucks)
    
    timestamp = datetime.now().isoformat()
    return {
        'Team': team_name,
        'Stadium': std_name,
        'Lat': lat,
        'Lng': lng,
        'Dunkin_Stats': d_stats,
        'Starbucks_Stats': s_stats,
        'Timestamp': timestamp
    }

def analyze_coffee_wars():
    bq_client = get_bq_client()
    if not bq_client: return

    # 1. Build Comprehensive Stadium List
    all_stadiums = []
    # Add Current
    for s in CURRENT_STADIUMS:
        all_stadiums.append({
            'Team': s['Team'], 'Stadium': s['Stadium'], 'StadiumLat': s['Lat'], 'StadiumLng': s['Lng']
        })
    # Add Manual/Historical
    existing_names = set(s['Stadium'] for s in all_stadiums)
    for name, data in MANUAL_STADIUM_COORDS.items():
        if name not in existing_names:
            all_stadiums.append({
                'Team': data.get('team', 'Historical'),
                'Stadium': name,
                'StadiumLat': data['lat'],
                'StadiumLng': data['lng']
            })
            
    print(f"Total Stadiums to Analyze: {len(all_stadiums)}")
    
    CACHE_FILE = os.path.join(os.path.dirname(__file__), "coffee_data_cache.json")
    results = []

    if os.path.exists(CACHE_FILE):
        print(f"Loading data from cache: {CACHE_FILE}")
        with open(CACHE_FILE, 'r') as f:
            results = json.load(f)
    else:
        # 2. Multiprocessing
        pool_size = 4 
        with multiprocessing.Pool(pool_size) as pool:
            results = pool.map(process_stadium, all_stadiums)
            
        results = [r for r in results if r]
        
        # Save Cache
        with open(CACHE_FILE, 'w') as f:
            json.dump(results, f)
            
    # 3. Save to BigQuery
    rows_to_insert = []
    
    for res in results:
        tn = res['Team']
        sn = res['Stadium']
        ts = res['Timestamp']
        
        row = {
            "team_name": tn, 
            "stadium_name": sn, 
            "updated_at": ts,
            "dunkin": res['Dunkin_Stats'],
            "starbucks": res['Starbucks_Stats']
        }
        rows_to_insert.append(row)

    # Prepare BQ Table (Single Row Per Stadium Schema)
    try:
        table_id = f"{BQ_PROJECT}.{BQ_TABLE}"
        bq_client.delete_table(table_id, not_found_ok=True)
        print(f"Dropped old table {table_id}")
    except Exception as e:
        print(f"Error dropping table: {e}")

    stats_schema = [
        bigquery.SchemaField("count_10mi", "INTEGER"),
        bigquery.SchemaField("closest_miles", "FLOAT"),
        bigquery.SchemaField("closest_location_name", "STRING"),
        bigquery.SchemaField(
            "locations", "RECORD", mode="REPEATED", fields=[
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("lat", "FLOAT"),
                bigquery.SchemaField("lng", "FLOAT"),
                bigquery.SchemaField("distance_miles", "FLOAT"),
            ]
        )
    ]

    schema = [
        bigquery.SchemaField("team_name", "STRING"),
        bigquery.SchemaField("stadium_name", "STRING"),
        bigquery.SchemaField("updated_at", "TIMESTAMP"),
        bigquery.SchemaField("dunkin", "RECORD", fields=stats_schema),
        bigquery.SchemaField("starbucks", "RECORD", fields=stats_schema),
    ]
    
    table = bigquery.Table(table_id, schema=schema)
    bq_client.create_table(table)
    print(f"Created new table {table_id}")

    print(f"Uploading {len(rows_to_insert)} rows to BigQuery...")
    # Use Load Job instead of Streaming Insert for reliability
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_TRUNCATE" # Overwrite if exists (though we deleted it)
    )
    
    try:
        job = bq_client.load_table_from_json(
            rows_to_insert, 
            table_id, 
            job_config=job_config
        )
        job.result() # Wait for completion
        print(f"Loaded {job.output_rows} rows to {table_id}")
    except Exception as e:
        print(f"Error loading table: {e}")
        # Debug: check error details
        if hasattr(e, 'errors'):
            print(e.errors)
        
    print("Data upload complete.")

if __name__ == "__main__":
    analyze_coffee_wars()
