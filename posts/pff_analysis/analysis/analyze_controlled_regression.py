import pandas as pd
import statsmodels.api as sm
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
SHEET_NAME = 'PFF Run Blocking Data'
MERGED_TAB = 'Merged Analysis Data'
OUTPUT_CSV = os.path.join(SCRIPT_DIR, '../data/player_controlled_regression_results.csv')

def fetch_from_sheets(tab_name):
    print(f"Fetching data from Google Sheet '{SHEET_NAME}', tab '{tab_name}'...")
    
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found.")
        return None

    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(tab_name)
        
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        print(f"  -> Loaded {len(df)} rows from Sheets.")
        return df
    except Exception as e:
        print(f"Error fetching from Sheets: {e}")
        return None

def main():
    # 1. Fetch Data from Sheets
    df = fetch_from_sheets(MERGED_TAB)
    if df is None: return
    
    # Required columns (Raw Distances)
    req_cols = ['Player', 'Grade', 'DistToIHOP', 'DrivingDist', 'DrivingTimeSeconds', 'SnapCount_RunBlock', 'IsHome', 'YearsInLeague', 'OppRunDefGrade']
    if not all(col in df.columns for col in req_cols):
        print(f"Error: Missing columns. Need {req_cols}")
        print(f"Available: {df.columns.tolist()}")
        return

    # Ensure numeric
    for col in req_cols:
        if col != 'Player':
            # Special handling for IsHome
            if col == 'IsHome':
                df[col] = df[col].map({'TRUE': 1, 'FALSE': 0, True: 1, False: 0, 1: 1, 0: 0, '1': 1, '0': 0})
            
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop NaNs in IsHome
    df = df.dropna(subset=['IsHome'])
    
    # Convert IsHome to int (0/1)
    df['IsHome'] = df['IsHome'].astype(int)
    
    # Filter 1: Observation Level (Snaps >= 10)
    df = df[df['SnapCount_RunBlock'] >= 10]
    
    # Identify Veterans (>= 100 Total Games)
    player_counts = df['Player'].value_counts()
    veterans = player_counts[player_counts >= 100].index
    print(f"Identified {len(veterans)} veterans with >= 100 total games.")
    
    # Filter for Veterans
    df = df[df['Player'].isin(veterans)]
    print(f"Data loaded and filtered (Snaps >= 10, Veterans Only): {len(df)} rows.")
    
    # Metrics to analyze (Raw Distances)
    metrics = [
        ('DistToIHOP', 'Haversine'),
        ('DrivingDist', 'DrivingDist'),
        ('DrivingTimeSeconds', 'DrivingTime')
    ]
    
    results = []
    
    players = df['Player'].unique()
    print(f"Analyzing {len(players)} veterans across {len(metrics)} metrics...")
    
    for metric_col, metric_name in metrics:
        print(f"  -> Processing {metric_name}...")
        
        # Drop NaNs for this specific metric AND Controls
        metric_df = df.dropna(subset=['Grade', metric_col, 'YearsInLeague', 'OppRunDefGrade'])
        
        # Add Quadratic Experience Term
        metric_df['YearsInLeague_Sq'] = metric_df['YearsInLeague'] ** 2
        
        for player in players:
            player_df = metric_df[metric_df['Player'] == player]
            
            n = len(player_df)
            
            # Ensure enough data points (>= 30 total games for regression stability)
            if n < 30:
                continue
            
            # Define X and Y
            # X = [Constant, Distance, IsHome, YearsInLeague, YearsInLeague_Sq, OppRunDefGrade]
            X = player_df[[metric_col, 'IsHome', 'YearsInLeague', 'YearsInLeague_Sq', 'OppRunDefGrade']]
            X = sm.add_constant(X) # Adds a column of 1s for intercept
            y = player_df['Grade']
            
            # Check for variance in metric (e.g. if all games are same distance)
            if player_df[metric_col].nunique() <= 1:
                continue
                
            try:
                model = sm.OLS(y, X).fit()
                
                # Extract coefficients and p-values
                dist_coef = model.params.get(metric_col)
                dist_pval = model.pvalues.get(metric_col)
                
                home_coef = model.params.get('IsHome')
                home_pval = model.pvalues.get('IsHome')
                
                exp_coef = model.params.get('YearsInLeague')
                exp_pval = model.pvalues.get('YearsInLeague')
                
                exp_sq_coef = model.params.get('YearsInLeague_Sq')
                exp_sq_pval = model.pvalues.get('YearsInLeague_Sq')

                opp_grade_coef = model.params.get('OppRunDefGrade')
                opp_grade_pval = model.pvalues.get('OppRunDefGrade')
                
                if dist_coef is None: continue

                results.append({
                    'Player': player,
                    'Metric': metric_name,
                    'Dist_Coef': dist_coef,
                    'Dist_PValue': dist_pval,
                    'IsHome_Coef': home_coef,
                    'IsHome_PValue': home_pval,
                    'Exp_Coef': exp_coef,
                    'Exp_PValue': exp_pval,
                    'Exp_Sq_Coef': exp_sq_coef,
                    'Exp_Sq_PValue': exp_sq_pval,
                    'OppRunDefGrade_Coef': opp_grade_coef,
                    'OppRunDefGrade_PValue': opp_grade_pval,
                    'R_Squared': model.rsquared,
                    'N_Games': n
                })
            except Exception as e:
                # print(f"Error for {player}: {e}")
                continue
        
    results_df = pd.DataFrame(results)
    
    # Save
    results_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved controlled regression results to {OUTPUT_CSV}")
    
    # Preview Leaders (Significant Distance Effect)
    for _, metric_name in metrics:
        print(f"\n{'='*60}")
        print(f"METRIC: {metric_name} (Controlled for IsHome + YearsInLeague + OppRunDefGrade)")
        print(f"{'='*60}")
        
        subset = results_df[(results_df['Metric'] == metric_name) & (results_df['Dist_PValue'] <= 0.05)]
        
        if subset.empty:
            print("No significant results found.")
            continue
            
        print(f"\n--- Top 5: Closer = Better (Negative Dist_Coef, p<=0.05) ---")
        top_closer = subset.sort_values(by='Dist_Coef', ascending=True).head(5)
        print(top_closer[['Player', 'Dist_Coef', 'Dist_PValue', 'IsHome_Coef', 'Exp_Coef', 'OppRunDefGrade_Coef', 'N_Games']].to_string(index=False))
        
        print(f"\n--- Top 5: Farther = Better (Positive Dist_Coef, p<=0.05) ---")
        top_farther = subset.sort_values(by='Dist_Coef', ascending=False).head(5)
        print(top_farther[['Player', 'Dist_Coef', 'Dist_PValue', 'IsHome_Coef', 'Exp_Coef', 'OppRunDefGrade_Coef', 'N_Games']].to_string(index=False))

if __name__ == "__main__":
    main()
