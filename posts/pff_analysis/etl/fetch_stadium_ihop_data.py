import os
import pandas as pd
import googlemaps
import math
import time

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
OUTPUT_CSV = os.path.join(SCRIPT_DIR, '../data/nfl_stadium_ihop_distances.csv')

# --- Helper Functions ---

def get_google_maps_client():
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    # Fallback to key file
    key_file_path = os.path.join(PROJECT_ROOT, 'shhhh/google_maps_api.key')
    if not api_key and os.path.exists(key_file_path):
        try:
            with open(key_file_path, 'r') as f:
                api_key = f.read().strip()
        except Exception as e:
            print(f"Error reading key file: {e}")

    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY environment variable not set and shhhh/google_maps_api.key not found.")
        return None
    return googlemaps.Client(key=api_key)

def haversine_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 3956 # Miles
    return c * r

def find_closest_ihop(gmaps, lat, lng):
    try:
        places_result = gmaps.places_nearby(
            location=(lat, lng),
            keyword='IHOP',
            rank_by='distance',
            type='restaurant'
        )
        if places_result.get('results'):
            for place in places_result['results']:
                name = place.get('name', '')
                if 'IHOP' in name.upper():
                    loc = place['geometry']['location']
                    return {
                        'name': name,
                        'address': place.get('vicinity'),
                        'lat': loc['lat'],
                        'lng': loc['lng']
                    }
        return None
    except Exception as e:
        print(f"Error finding IHOP: {e}")
        return None

def get_driving_distance(gmaps_client, origin_lat, origin_lng, dest_lat, dest_lng):
    """
    Calculates driving distance and duration using Google Maps Distance Matrix API.
    """
    try:
        result = gmaps_client.distance_matrix(
            origins=(origin_lat, origin_lng),
            destinations=(dest_lat, dest_lng),
            mode="driving",
            units="imperial"
        )
        
        if result['status'] == 'OK':
            element = result['rows'][0]['elements'][0]
            if element['status'] == 'OK':
                distance_text = element['distance']['text']
                distance_val = element['distance']['value'] # meters
                duration_text = element['duration']['text']
                duration_val = element['duration']['value'] # seconds
                
                # Convert meters to miles
                distance_miles = distance_val * 0.000621371
                
                return {
                    'text_dist': distance_text,
                    'val_dist': distance_miles,
                    'text_dur': duration_text,
                    'val_dur': duration_val
                }
        return None
    except Exception as e:
        print(f"Error calculating driving distance: {e}")
        return None

def main():
    # Hardcoded coordinates from notebook (reliable)
    nfl_stadiums = [
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
    
    gmaps = get_google_maps_client()
    if not gmaps:
        return

    results = []
    print(f"Processing {len(nfl_stadiums)} stadiums...")

    for team_data in nfl_stadiums:
        team = team_data['Team']
        stadium = team_data['Stadium']
        lat = team_data['Lat']
        lng = team_data['Lng']
        
        print(f"Processing {team} ({stadium})...")
        
        ihop = find_closest_ihop(gmaps, lat, lng)
        
        row = {
            'Team': team,
            'Stadium': stadium,
            'StadiumLat': lat,
            'StadiumLng': lng,
            'IHOP_Name': None,
            'IHOP_Address': None,
            'IHOP_Lat': None,
            'IHOP_Lng': None,
            'HaversineDist': None,
            'DrivingDist': None,
            'DrivingTime': None,
            'DrivingTimeSeconds': None
        }

        if ihop:
            row['IHOP_Name'] = ihop['name']
            row['IHOP_Address'] = ihop['address']
            row['IHOP_Lat'] = ihop['lat']
            row['IHOP_Lng'] = ihop['lng']
            
            # 1. Haversine
            h_dist = haversine_distance(lat, lng, ihop['lat'], ihop['lng'])
            row['HaversineDist'] = round(h_dist, 2)
            
            # 2. Driving
            drive_data = get_driving_distance(gmaps, lat, lng, ihop['lat'], ihop['lng'])
            if drive_data:
                row['DrivingDist'] = round(drive_data['val_dist'], 2)
                row['DrivingTime'] = drive_data['text_dur']
                row['DrivingTimeSeconds'] = drive_data['val_dur']
                print(f"  -> Found IHOP: {h_dist:.2f} mi (Haversine), {drive_data['val_dist']:.2f} mi (Driving)")
            else:
                print(f"  -> Found IHOP: {h_dist:.2f} mi (Haversine), Driving N/A")
        else:
            print("  -> No IHOP found.")
        
        results.append(row)
        time.sleep(0.1) # Rate limit niceness

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved results to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
