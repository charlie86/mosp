
import sys
import os
import pandas as pd
from datetime import datetime

from posts.stuperlatives.etl.bq_utils import get_bq_client
from posts.stuperlatives.analysis.mascot_analysis import (
    analyze_bird_hunters,
    analyze_circus_tamers,
    analyze_social_justice_warriors,
    analyze_deadliest_catch,
    analyze_pirates_booty,
    analyze_schoolyard_bullies
)
from posts.stuperlatives.analysis.appearance_analysis import (
    analyze_grizzly_adams,
    analyze_yosemite_sam,
    analyze_rooster_fever
)

REPORT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(REPORT_DIR, "report.md")

def df_to_markdown_table(df):
    if df.empty:
        return "*No Results Found*\n"
    return df.to_markdown(index=False) + "\n"

def generate_report():
    print("Generating Stuperlatives Report (BigQuery Edition)...")
    
    # 1. Setup BQ Client
    client = get_bq_client()
    if not client:
        print("Error: Could not obtain BigQuery client. Ensure service_account.json exists.")
        return

    report_content = f"# Stuperlatives Analysis Report\n"
    report_content += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    report_content += "This report contains the raw numbers and winners for each arbitrary superlative category (Calculated via BigQuery).\n\n"
    
    # --- MASCOT ANALYSIS ---
    report_content += "## I. Mascot-Based Metrics\n"
    report_content += "*(Analysis Period: 1999-2025)*\n\n"
    
    # Bird Hunters
    try:
        df_birds = analyze_bird_hunters(client)
        report_content += "### 1. Bird Hunters\n"
        report_content += "*Metric: Total Passes Defended + INTs against Bird Teams.*\n"
        report_content += "**Bird Teams:** Cardinals (ARI), Falcons (ATL), Ravens (BAL), Eagles (PHI), Seahawks (SEA)\n\n"
        report_content += df_to_markdown_table(df_birds) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"

    # Circus Tamers
    try:
        df_circus = analyze_circus_tamers(client)
        report_content += "### 2. Circus Tamers\n"
        report_content += "*Metric: Fewest Rushing Yards Allowed/Game against Circus Teams (min 2 games).*\n"
        report_content += "**Circus Teams:** Lions (DET), Bears (CHI), Bengals (CIN), Jaguars (JAX)\n\n"
        report_content += df_to_markdown_table(df_circus) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"

    # Social Justice Warriors
    try:
        df_sjw = analyze_social_justice_warriors(client)
        report_content += "### 3. Social Justice Warriors\n"
        report_content += "*Metric: Highest Win % against Social Justice Teams (min 3 games).*\n"
        report_content += "**Teams:** Chiefs (KC), Redskins (WAS, 1999-2019 only)\n\n"
        report_content += df_to_markdown_table(df_sjw) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"

    # Deadliest Catch
    try:
        df_catch = analyze_deadliest_catch(client)
        report_content += "### 4. Deadliest Catch\n"
        report_content += "*Metric: Total Interceptions against Aquatic Teams.*\n"
        report_content += "**Aquatic Teams:** Dolphins (MIA), Seahawks (SEA), Chargers (LAC/SD)\n\n"
        report_content += df_to_markdown_table(df_catch) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"
        
    # Pirate's Booty
    try:
        df_booty = analyze_pirates_booty(client)
        report_content += "### 5. Pirate's Booty\n"
        report_content += "*Metric: Total Takeaways/Game by Pirate Defenses.*\n"
        report_content += "**Pirate Teams:** Buccaneers (TB), Raiders (LV/OAK), Vikings (MIN)\n\n"
        report_content += df_to_markdown_table(df_booty) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"
        
    # Schoolyard Bullies
    try:
        df_bullies = analyze_schoolyard_bullies(client)
        report_content += "### 9. Schoolyard Bullies\n"
        report_content += "*Metric: Total Tackles against Ivy League graduates.*\n"
        report_content += "**Targets:** Players from Brown, Columbia, Cornell, Dartmouth, Harvard, Penn, Princeton, Yale\n\n"
        report_content += df_to_markdown_table(df_bullies) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"

    # --- APPEARANCE ANALYSIS ---
    report_content += "## II. Appearance-Based Metrics (Gemini Vision)\n"
    report_content += "*(Analysis Period: 1999-2025)*\n\n"
    
    # Grizzly Adams
    try:
        df_beard = analyze_grizzly_adams(client)
        report_content += "### 6. Grizzly Adams\n"
        report_content += "*Metric: Total Tackles by Bearded Defenders.*\n"
        report_content += "*Note: Appearance data is inferred from available headshots. Players without a detectable beard in their profile photo are excluded.*\n\n"
        report_content += df_to_markdown_table(df_beard) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"

    # Yosemite Sam
    try:
        df_stache = analyze_yosemite_sam(client)
        report_content += "### 7. Yosemite Sam\n"
        report_content += "*Metric: EPA/Play for Mustached QBs (No Beard).*\n"
        report_content += "*Note: Only includes QBs with a mustache and NO beard in their official headshot.*\n\n"
        report_content += df_to_markdown_table(df_stache) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"
        
    # Rooster Fever
    try:
        df_rooster = analyze_rooster_fever(client)
        report_content += "### 8. Rooster Fever\n"
        report_content += "*Metric: Total Sacks recorded by defenders against Redheaded QBs.*\n"
        report_content += "**Targets:** Redheaded QBs identified via vision analysis (e.g. Andy Dalton, Carson Wentz, etc.)\n\n"
        report_content += df_to_markdown_table(df_rooster) + "\n"
    except Exception as e:
        report_content += f"Error: {e}\n\n"

    # Save Report
    with open(REPORT_PATH, 'w') as f:
        f.write(report_content)
        
    print(f"Report generated at {REPORT_PATH}")

if __name__ == "__main__":
    generate_report()
