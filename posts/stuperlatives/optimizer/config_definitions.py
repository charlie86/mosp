
import os
import json

# --- Data Loading Helper ---
def load_ihop_teams():
    # Path relative to this file: ../../pff_analysis/data/stadium_gravitational_data.json
    # current file is in posts/stuperlatives/optimizer/
    base_dir = os.path.dirname(__file__)
    json_path = os.path.abspath(os.path.join(base_dir, '../../pff_analysis/data/stadium_gravitational_data.json'))
    
    TEAM_NAME_TO_ABBR = {
        'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL', 'Buffalo Bills': 'BUF',
        'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE',
        'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
        'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KC',
        'Las Vegas Raiders': 'LV', 'Los Angeles Chargers': 'LAC', 'Los Angeles Rams': 'LAR', 'Miami Dolphins': 'MIA',
        'Minnesota Vikings': 'MIN', 'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG',
        'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 'San Francisco 49ers': 'SF',
        'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB', 'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS',
        'Washington Football Team': 'WAS', 'Washington Redskins': 'WAS' 
    }
    
    ihop_teams = set()
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
                for entry in data:
                    team_name = entry.get('Team')
                    ihops = entry.get('IHOPs', [])
                    # Check if any IHOP is within 5 miles
                    has_close_ihop = any(i.get('DistanceMiles', 100) < 5.0 for i in ihops)
                    if has_close_ihop and team_name in TEAM_NAME_TO_ABBR:
                        ihop_teams.add(TEAM_NAME_TO_ABBR[team_name])
        else:
            print(f"Warning: IHOP data file not found at {json_path}")
    except Exception as e:
        print(f"Error loading IHOP data: {e}")
        return []
    return list(ihop_teams)

# Load IHOP Teams globally
IHOP_TEAMS = load_ihop_teams()
IHOP_FILTER_STR = "1=0" # Default false if no teams
if IHOP_TEAMS:
    # Proper SQL formatting for IN clause
    teams_formatted = "', '".join(IHOP_TEAMS)
    IHOP_FILTER_STR = f"home_team IN ('{teams_formatted}')"


# Geographic Mappings
REGION_MAPPING = {
    'West': ['SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD'],
    'Midwest': ['GB', 'CHI', 'MIN', 'DET', 'IND', 'CIN', 'CLE', 'KC', 'STL'],
    'South': ['DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN'],
    'NorthEast': ['NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS']
}

# Team Categories
HAT_TEAMS = ['NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK'] # Mascots with Hats (Patriot, Pirate, Cowboy, Prospector, Hard Hat, Commander, Viking, Raider)
BIRD_TEAMS = ['ARI', 'ATL', 'BAL', 'PHI', 'SEA']


# Metrics by Position
# Tuple Format: (SQL_Calculation, Sort_Direction)
METRICS = {
    'QB': {
        'Passing Yards/Game': ('SUM(yards_gained)/COUNT(DISTINCT game_id)', 'DESC'),
        'TDs/Game': ('SUM(touchdown)/COUNT(DISTINCT game_id)', 'DESC'),
        'Completion %': ('SUM(complete_pass)/COUNT(*)', 'DESC'),
        'Yards/Attempt': ('SUM(yards_gained)/COUNT(*)', 'DESC'),
        'EPA/Play': ('AVG(epa)', 'DESC'),
        'Success Rate': ('SUM(success)/COUNT(*)', 'DESC'),
        'CPOE': ('AVG(cpoe)', 'DESC'),
        'TD/INT Ratio': ('CAST(SUM(touchdown) AS FLOAT64) / NULLIF(SUM(interception), 0)', 'DESC'),
        'Lowest INT Rate': ('SUM(interception)/COUNT(*)', 'ASC')
    },
    'RB': {
        'Yards/Game': ('SUM(yards_gained)/COUNT(DISTINCT game_id)', 'DESC'),
        'Yards/Carry': ('SUM(yards_gained)/COUNT(*)', 'DESC'),
        'Touchdowns': ('SUM(touchdown)', 'DESC'),
        'EPA/Rush': ('AVG(epa)', 'DESC'),
        'Success Rate': ('SUM(success)/COUNT(*)', 'DESC')
    },
    'WR': {
        'Yards/Game': ('SUM(yards_gained)/COUNT(DISTINCT game_id)', 'DESC'),
        'Yards/Target': ('SUM(yards_gained)/COUNT(*)', 'DESC'),
        'Catch Rate': ('SUM(complete_pass)/COUNT(*)', 'DESC'),
        'Touchdowns': ('SUM(touchdown)', 'DESC'),
        'EPA/Target': ('AVG(epa)', 'DESC')
    }
}

# Base Filters (Common to all positions)
BASE_FILTERS = {
    'Game Context': {
        'All': '1=1',
        'Ahead': 'score_differential > 0',
        'Behind': 'score_differential < 0',
        'Tied': 'score_differential = 0',
        '4th Quarter': 'qtr = 4',
        'Overtime': 'qtr = 5',
        'One Score Game': 'ABS(score_differential) <= 8'
    },
    'Down': {
        'All': '1=1',
        '1st Down': 'down = 1',
        '2nd Down': 'down = 2',
        '3rd Down': 'down = 3',
        '4th Down': 'down = 4',
        'Money Down': 'down >= 3'
    },
    'Field Position': {
        'All': '1=1',
        'Red Zone': 'yardline_100 <= 20',
        'Own Territory': 'yardline_100 > 50',
        'Opponent Territory': 'yardline_100 <= 50',
        'Deep Own Terr': 'yardline_100 > 80'
    },
    'Opponent': {
        'All': '1=1',
        'Pirate Teams': "defteam IN ('TB', 'MIN', 'LV', 'OAK')",
        'Bird Teams': "defteam IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')",
        'Hat Teams': "defteam IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')",
        'Cat Teams': "defteam IN ('DET', 'JAX', 'CAR', 'CIN')",
        'Division Rivals': 'div_game = 1',
    },
    'Environment': {
        'All': '1=1',
        'Night Game': "start_time > '19:00:00'",
        'Dome': "roof IN ('dome', 'closed')",
        'Outdoors': "roof = 'outdoors'",
        'Within 5mi of IHOP': IHOP_FILTER_STR
    },
    'Venue': {
        'All': '1=1',
        'Home': 'posteam = home_team',
        'Away': 'posteam = away_team'
    }
}

# Position Specific Filters
POSITION_FILTERS = {
    'QB': {
        'Direction': {
             'All': '1=1',
             'Left': "pass_location = 'left'",
             'Middle': "pass_location = 'middle'",
             'Right': "pass_location = 'right'"
        }
    },
    'RB': {
        'Run Direction': {
             'All': '1=1',
             'Left': "run_location = 'left'",
             'Middle': "run_location = 'middle'",
             'Right': "run_location = 'right'"
        }
    },
    'WR': {
        'Route Area': {
             'All': '1=1',
             'Deep': "air_yards >= 20",
             'Short': "air_yards < 10"
        }
    }
}
