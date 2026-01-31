
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pandas as pd
import os

# Configuration
PROJECT_ROOT = "/Users/charliethompson/Documents/mosp"
DATA_FILE = os.path.join(PROJECT_ROOT, "posts/stuperlatives/super_bowl/prep/coffee_data_cache.json")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "posts/stuperlatives/super_bowl/final_coffee_gravity_ranking.png")
LOGO_DIR = os.path.join(PROJECT_ROOT, "posts/stuperlatives/super_bowl/logos")

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
    "Philadelphia Eagles": "Lincoln Financial Field",
    "Pittsburgh Steelers": "Acrisure Stadium",
    "San Francisco 49ers": "Levi's Stadium",
    "Seattle Seahawks": "Lumen Field",
    "Tampa Bay Buccaneers": "Raymond James Stadium",
    "Tennessee Titans": "Nissan Stadium",
    "Washington Commanders": "Commanders Field",
}

TEAM_ABBR_MAPPING = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS",
}

def simple_hav(lo1, la1, lo2, la2):
    """Haversine distance in miles"""
    from math import radians, sin, cos, asin, sqrt
    lo1, la1, lo2, la2 = map(radians, [lo1, la1, lo2, la2])
    dlon = lo2 - lo1
    dlat = la2 - la1
    a = sin(dlat/2)**2 + cos(la1) * cos(la2) * sin(dlon/2)**2
    return 2 * asin(sqrt(a)) * 3956

def calculate_stadium_gravity_single(stadium_lat, stadium_lng, d_locs, s_locs):
    """
    Calculate net gravity at a stadium using the interference model
    Returns: (dunkin_gravity, starbucks_gravity, net_gravity)
    """
    INTERFERENCE_RADIUS = 0.5  # miles
    INTERFERENCE_STRENGTH = 1.0
    
    if len(d_locs) == 0 and len(s_locs) == 0:
        return 0.0, 0.0, 0.0
    
    # Initialize masses
    d_masses = np.ones(len(d_locs))
    s_masses = np.ones(len(s_locs))
    
    # Apply interference reduction
    if len(d_locs) > 0 and len(s_locs) > 0:
        for i, d in enumerate(d_locs):
            for j, s in enumerate(s_locs):
                dist = simple_hav(d['lng'], d['lat'], s['lng'], s['lat'])
                if dist < INTERFERENCE_RADIUS:
                    reduction = INTERFERENCE_STRENGTH * (1.0 - dist/INTERFERENCE_RADIUS)
                    d_masses[i] -= reduction
                    s_masses[j] -= reduction
        d_masses = np.maximum(d_masses, 0.0)
        s_masses = np.maximum(s_masses, 0.0)
    
    # Calculate gravity at stadium location
    dunkin_gravity = 0.0
    starbucks_gravity = 0.0
    
    for i, loc in enumerate(d_locs):
        if d_masses[i] > 0:
            dist = simple_hav(loc['lng'], loc['lat'], stadium_lng, stadium_lat)
            dunkin_gravity += d_masses[i] * np.exp(-0.5 * dist)
    
    for i, loc in enumerate(s_locs):
        if s_masses[i] > 0:
            dist = simple_hav(loc['lng'], loc['lat'], stadium_lng, stadium_lat)
            starbucks_gravity += s_masses[i] * np.exp(-0.5 * dist)
    
    # Net Gravity: Starbucks (Positive) - Dunkin (Negative)
    # User requested: "starbucks is positive and dunkin negative"
    net_gravity = starbucks_gravity - dunkin_gravity
    return dunkin_gravity, starbucks_gravity, net_gravity

def get_logo_image(team_name, target_size=50):
    """
    Load team logo and return an OffsetImage normalized to target_size (approx pixels of visible content).
    """
    abbr = TEAM_ABBR_MAPPING.get(team_name)
    if not abbr:
        print(f"No abbreviation for {team_name}")
        return None
    
    path = os.path.join(LOGO_DIR, f"{abbr}.png")
    if not os.path.exists(path):
        print(f"No logo file found for {team_name} ({path})")
        return None
    
    img = plt.imread(path)
    
    # Calculate visible content dimensions based on alpha channel
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        rows = np.any(alpha > 0.05, axis=1)
        cols = np.any(alpha > 0.05, axis=0)
        r = np.where(rows)[0]
        c = np.where(cols)[0]
        if len(r) > 0 and len(c) > 0:
            h_content = r[-1] - r[0]
            w_content = c[-1] - c[0]
            max_dim_content = max(h_content, w_content)
        else:
            max_dim_content = max(img.shape[:2])
    else:
        max_dim_content = max(img.shape[:2])
    
    # Target zoom based on CONTENT size, not CANVAS size
    zoom = target_size / max_dim_content
    
    return OffsetImage(img, zoom=zoom)

def main():
    # Load data
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    results = []

    print(f"Loaded {len(data)} entries from cache.")

    for entry in data:
        team = entry['Team']
        stadium = entry['Stadium']
        
        # Deduplicate and Filter
        if team not in TARGET_STADIUMS:
            continue
        if TARGET_STADIUMS[team] != stadium:
            continue
        
        lat = entry['Lat']
        lng = entry['Lng']
        
        d_locs = entry.get('Dunkin_Stats', {}).get('locations', [])
        s_locs = entry.get('Starbucks_Stats', {}).get('locations', [])
        
        d_grav, s_grav, net_grav = calculate_stadium_gravity_single(lat, lng, d_locs, s_locs)
        
        results.append({
            'Team': team,
            'Stadium': stadium,
            'Dunkin Gravity': d_grav,
            'Starbucks Gravity': s_grav,
            'Net Gravity': net_grav
        })
    
    df = pd.DataFrame(results)
    
    # Group by Stadium to handle shared stadiums (MetLife, SoFi)
    grouped = []
    
    for stadium, group in df.groupby('Stadium'):
        first = group.iloc[0]
        teams = group['Team'].tolist()
        
        grouped.append({
            'Stadium': stadium,
            'Teams': teams, # List of teams
            'Dunkin Gravity': first['Dunkin Gravity'],
            'Starbucks Gravity': first['Starbucks Gravity'],
            'Net Gravity': first['Net Gravity']
        })
        
    df = pd.DataFrame(grouped)
    
    # Sort by Net Gravity 
    df = df.sort_values('Net Gravity', ascending=True).reset_index(drop=True)
    
    # Calculate global max gravity for symmetric axis limits
    max_dunkin = df['Dunkin Gravity'].max()
    max_starbucks = df['Starbucks Gravity'].max()
    global_max_grav = max(max_dunkin, max_starbucks)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(18, 24))
    
    y_pos = np.arange(len(df))
    
    # Space for logos in the center
    X_OFFSET = 1.1
    
    # Colors
    SB_SOLID = '#00704A'
    SB_LIGHT = '#00704A4D' # 30% alpha roughly
    DD_SOLID = '#FF671F'
    DD_LIGHT = '#FF671F4D' # 30% alpha roughly
    
    # Initialize arrays for stacked plotting
    sb_solid = np.zeros(len(df))
    sb_remain = np.zeros(len(df))
    sb_loss = np.zeros(len(df))
    
    dd_solid = np.zeros(len(df))
    dd_remain = np.zeros(len(df))
    dd_loss = np.zeros(len(df))
    
    for i, row in df.iterrows():
        net = row['Net Gravity']
        s_grav = row['Starbucks Gravity']
        d_grav = row['Dunkin Gravity']
        
        if net > 0:
            sb_solid[i] = net
            sb_remain[i] = s_grav - net
            dd_loss[i] = d_grav
        else:
            net_mag = abs(net)
            dd_solid[i] = net_mag
            dd_remain[i] = d_grav - net_mag
            sb_loss[i] = s_grav
            
    # Starbucks Side (Right / Positive)
    # Start all bars at X_OFFSET
    ax.barh(y_pos, sb_solid, color=SB_SOLID, height=0.6, left=X_OFFSET)
    ax.barh(y_pos, sb_remain, color=SB_LIGHT, height=0.6, left=X_OFFSET + sb_solid)
    ax.barh(y_pos, sb_loss, color=SB_LIGHT, height=0.6, left=X_OFFSET)
    
    # Dunkin Side (Left / Negative)
    # Start all bars at -X_OFFSET
    ax.barh(y_pos, -dd_solid, color=DD_SOLID, height=0.6, left=-X_OFFSET)
    ax.barh(y_pos, -dd_remain, color=DD_LIGHT, height=0.6, left=-X_OFFSET - dd_solid)
    ax.barh(y_pos, -dd_loss, color=DD_LIGHT, height=0.6, left=-X_OFFSET)
    
    # Axis formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels([]) # Hide text labels
    ax.set_xlabel('Gravity Score', fontsize=32, fontweight='bold', labelpad=20)
    
    # Main title (bold, large) and subtitle (italic, smaller) with explicit positioning
    # Moved down to provide whitespace at the top
    fig.text(0.5, 0.96, "Home Brew Advantage", ha='center', fontsize=48, fontweight='bold')
    fig.text(0.5, 0.93, "Net gravity of Starbucks vs Dunkin' locations within 10 miles of NFL stadiums", 
             ha='center', fontsize=26, style='italic')
    
    # Add top margin for titles (handled by tight_layout rect now)
    # plt.subplots_adjust(top=0.92)
    
    # Increase tick label size and length
    # User requested longer ticks
    ax.tick_params(axis='x', labelsize=24, length=12, width=2)
    
    # Remove Y-axis ticks (keep labels if any, though we use images mostly)
    ax.tick_params(axis='y', length=0)

    # Set explicit ticks at round numbers relative to X_OFFSET
    tick_step = 5
    # Calculate how many ticks we need based on the global limit
    limit = global_max_grav + X_OFFSET + 2.5
    # Start from tick_step (e.g. 5) instead of 0 to remove the '0' ticks at bar starts
    tick_vals = np.arange(tick_step, limit, tick_step)
    
    pos_ticks = X_OFFSET + tick_vals
    neg_ticks = -(X_OFFSET + tick_vals)
    # Keep the absolute zero in center, but exclude the offset zeros
    all_ticks = np.sort(np.concatenate([neg_ticks, [0], pos_ticks]))
    
    ax.set_xticks(all_ticks)
    
    # Absolute value x-axis labels (shifted by X_OFFSET)
    def shifted_abs_formatter(x, pos):
        if x > 0 and x >= X_OFFSET:
            val = x - X_OFFSET
        elif x < 0 and abs(x) >= X_OFFSET:
            val = abs(x) - X_OFFSET
        else:
            val = 0
        return f'{val:.0f}'
    
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(shifted_abs_formatter))

    
    # Add grid - User requested removal of grid lines at 5 and 10
    # ax.grid(axis='x', linestyle='--', alpha=0.3)
    
    # Add Logos in the CENTER
    logo_x = 0
    for i, row in df.iterrows():
        teams = row['Teams']
        y = i
        num_teams = len(teams)
        
        if num_teams == 1:
            logo = get_logo_image(teams[0], target_size=50)
            if logo:
                ab = AnnotationBbox(logo, (logo_x, y), frameon=False, box_alignment=(0.5, 0.5))
                ax.add_artist(ab)
        else:
            # Shift slightly to fit both in center and make them smaller
            SHARED_SIZE = 35
            logo_offset = 0.55
            logo1 = get_logo_image(teams[0], target_size=SHARED_SIZE)
            if logo1:
                ab1 = AnnotationBbox(logo1, (logo_x - logo_offset, y), frameon=False, box_alignment=(0.5, 0.5))
                ax.add_artist(ab1)
            logo2 = get_logo_image(teams[1], target_size=SHARED_SIZE)
            if logo2:
                ab2 = AnnotationBbox(logo2, (logo_x + logo_offset, y), frameon=False, box_alignment=(0.5, 0.5))
                ax.add_artist(ab2)
                
        # Add Data Label
        net = row['Net Gravity']
        if net > 0:
            label = f"+{net:.1f}"
            bar_end = X_OFFSET + net
            ax.text(bar_end + 0.15, y, label, va='center', ha='left', fontsize=16, fontweight='bold', color='#004b32')
        else:
            label = f"+{abs(net):.1f}"
            bar_end = -X_OFFSET - abs(net)
            ax.text(bar_end - 0.15, y, label, va='center', ha='right', fontsize=16, fontweight='bold', color='#cc5219')

    # Add crossover line (where Net Gravity switches from Negative to Positive)
    # df is sorted ascending, so we look for the first positive value
    crossover_indices = df.index[df['Net Gravity'] > 0].tolist()
    if crossover_indices:
        first_positive_idx = crossover_indices[0]
        # Draw line strictly between the last negative/zero and first positive
        # This is at index - 0.5. User requested move back to original position.
        # User requested slightly shorter dashes than 15: (0, (10, 10))
        ax.axhline(y=first_positive_idx - 0.5, color='black', linestyle=(0, (10, 10)), linewidth=2, alpha=0.5)

    # Symmetric limit including offset and padding
    limit = global_max_grav + X_OFFSET + 2.5
    ax.set_xlim(-limit, limit)
    # Tighten Y-axis to remove whitespace at top and bottom
    ax.set_ylim(-0.5, len(df) - 0.5)
    
    # Remove chart borders (spines) as requested ("Remove the box around the chart")
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Custom Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=SB_SOLID, label='Net Starbucks Gravity'),
        Patch(facecolor=SB_LIGHT, label='Neutralized Starbucks'),
        Patch(facecolor=DD_SOLID, label='Net Dunkin\' Gravity'),
        Patch(facecolor=DD_LIGHT, label='Neutralized Dunkin\'')
    ]
    # Remove legend box ("it should just be transparent")
    ax.legend(handles=legend_elements, loc='upper left', fontsize=28, frameon=False)
    
    # Reserve space for titles by adjusting the top of the layout rectangle
    # top=0.925 leaves 7.5% of the figure height for the title/subtitle
    # Subtitle is at 0.93, so this brings chart closer
    plt.tight_layout(rect=[0, 0, 1, 0.925])
    
    # Save with white background (default)
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Chart saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
