
import os
import sys
import pandas as pd
from google.cloud import bigquery
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.bq_utils import get_bq_client

# --- Configuration ---
TARGET_SEASON = 2025
BLOCKING_SUMMARY = f"pff_blocking_summary_{TARGET_SEASON}"
IHOP_TABLE = "stuperlatives.ihop_data"

client = get_bq_client()

print("Loading OL Data...")
ol_query = f"""
    SELECT 
        team_name, week,
        AVG(grades_offense) as unit_grade_offense,
        AVG(grades_pass_block) as unit_grade_pass_block,
        AVG(grades_run_block) as unit_grade_run_block,
        SUM(sacks_allowed) as unit_sacks_allowed,
        SUM(pressures_allowed) as unit_pressures_allowed,
        AVG(pbe) as unit_pbe
    FROM `pff_analysis.{BLOCKING_SUMMARY}`
    WHERE position IN ('T', 'G', 'C')
    GROUP BY team_name, week
"""
ol_df = client.query(ol_query).to_dataframe()

print("Loading Schedule & IHOP...")
schedule_query = f"""
    WITH ihop AS (
        SELECT Team, DistanceMiles FROM `{IHOP_TABLE}`
    )
    SELECT 
        s.season, s.week, s.posteam as team_name, 
        s.defteam as opponent,
        s.home_team,
        CAST(i.DistanceMiles AS FLOAT64) as dist_to_ihop
    FROM `stuperlatives.pbp_data` s
    LEFT JOIN ihop i ON s.home_team = i.Team
    WHERE s.season = {TARGET_SEASON}
    GROUP BY 1,2,3,4,5,6
"""
sched_df = client.query(schedule_query).to_dataframe()

df = pd.merge(ol_df, sched_df, on=['week', 'team_name'])

# --- Comparison Contexts ---
# We want to compare Near vs Far for each team
teams = ['NE', 'SEA']
splits = [
    ('Near IHOP (< 2mi)', 'dist_to_ihop <= 2.0'),
    ('Far from IHOP (> 2mi)', 'dist_to_ihop > 2.0')
]

output_file = "posts/stuperlatives/super_bowl/super_bowl_ol_ihop_split.md"
with open(output_file, "w") as f:
    f.write("# Super Bowl OL Analysis: The IHOP Effect\n\n")
    f.write("Comparing Offensive Line performance when playing within 2 miles of an IHOP versus away from one.\n\n")
    
    for team in teams:
        f.write(f"## {team} Offensive Line\n\n")
        
        team_stats = []
        for split_name, split_filter in splits:
            query_str = f"team_name == '{team}' and {split_filter}"
            data = df.query(query_str)
            
            if data.empty:
                 team_stats.append({
                    'Condition': split_name, 'Games': 0, 
                    'Pass Blk': '-', 'Run Blk': '-', 'Sacks/G': '-', 'Pressures/G': '-', 'PBE': '-'
                })
            else:
                team_stats.append({
                    'Condition': split_name,
                    'Games': len(data),
                    'Pass Blk': f"{data['unit_grade_pass_block'].median():.1f}",
                    'Run Blk': f"{data['unit_grade_run_block'].median():.1f}",
                    'Sacks/G': f"{data['unit_sacks_allowed'].mean():.1f}",
                    'Pressures/G': f"{data['unit_pressures_allowed'].mean():.1f}",
                    'PBE': f"{data['unit_pbe'].median():.1f}"
                })
        
        stat_df = pd.DataFrame(team_stats)
        f.write(stat_df.to_markdown(index=False))
        f.write("\n\n")

print(f"IHOP Split Analysis saved to {output_file}")
