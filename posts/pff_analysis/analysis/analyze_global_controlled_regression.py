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
    
    # Required columns
    req_cols = ['Grade', 'DistToIHOP', 'DrivingDist', 'DrivingTimeSeconds', 'SnapCount_RunBlock', 'IsHome', 'YearsInLeague', 'OppRunDefGrade']
    
    # Check for missing columns
    missing = [col for col in req_cols if col not in df.columns]
    if missing:
        print(f"Error: Missing columns: {missing}")
        return

    # Ensure numeric
    for col in req_cols:
        # Special handling for IsHome (might be boolean or string 'TRUE'/'FALSE')
        if col == 'IsHome':
            # Convert boolean/string boolean to int (0/1) first
            df[col] = df[col].map({'TRUE': 1, 'FALSE': 0, True: 1, False: 0, 1: 1, 0: 0, '1': 1, '0': 0})
        
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop NaNs in IsHome
    df = df.dropna(subset=['IsHome'])
    
    # Convert IsHome to int (0/1)
    df['IsHome'] = df['IsHome'].astype(int)
    
    # Add Quadratic Experience Term
    df['YearsInLeague_Sq'] = df['YearsInLeague'] ** 2
    
    # Filter 1: Observation Level (Snaps >= 10)
    df = df[df['SnapCount_RunBlock'] >= 10]
    print(f"Data loaded and filtered (Snaps >= 10): {len(df)} rows.")
    
    # Metrics to analyze (Raw Distances)
    metrics = [
        ('DistToIHOP', 'Haversine'),
        ('DrivingDist', 'DrivingDist'),
        ('DrivingTimeSeconds', 'DrivingTime')
    ]
    
    print("\n" + "="*60)
    print("GLOBAL CONTROLLED REGRESSION (All Players, Snaps >= 10)")
    print("Model: Grade ~ Distance + IsHome + YearsInLeague + YearsInLeague^2 + OppRunDefGrade")
    print("="*60)
    
    for metric_col, metric_name in metrics:
        # Drop NaNs for this specific metric AND controls
        metric_df = df.dropna(subset=['Grade', metric_col, 'YearsInLeague', 'YearsInLeague_Sq', 'OppRunDefGrade'])
        
        X = metric_df[[metric_col, 'IsHome', 'YearsInLeague', 'YearsInLeague_Sq', 'OppRunDefGrade']]
        X = sm.add_constant(X)
        y = metric_df['Grade']
        
        try:
            model = sm.OLS(y, X).fit()
            
            print(f"\nMETRIC: {metric_name}")
            print(f"Observations: {len(metric_df)}")
            print(f"R-Squared:    {model.rsquared:.6f}")
            
            # Distance Coef
            dist_coef = model.params[metric_col]
            dist_pval = model.pvalues[metric_col]
            print(f"Dist Coef:    {dist_coef:.6f} (p={dist_pval:.6f})")
            
            # IsHome Coef
            home_coef = model.params['IsHome']
            home_pval = model.pvalues['IsHome']
            print(f"IsHome Coef:  {home_coef:.6f} (p={home_pval:.6f})")
            
            # YearsInLeague Coef
            exp_coef = model.params['YearsInLeague']
            exp_pval = model.pvalues['YearsInLeague']
            print(f"Exp Coef:     {exp_coef:.6f} (p={exp_pval:.6f})")
            
            # YearsInLeague_Sq Coef
            exp_sq_coef = model.params['YearsInLeague_Sq']
            exp_sq_pval = model.pvalues['YearsInLeague_Sq']
            print(f"Exp^2 Coef:   {exp_sq_coef:.6f} (p={exp_sq_pval:.6f})")
            
            # OppRunDefGrade Coef
            def_coef = model.params['OppRunDefGrade']
            def_pval = model.pvalues['OppRunDefGrade']
            print(f"Def Coef:     {def_coef:.6f} (p={def_pval:.6f})")
            
            if dist_pval <= 0.05:
                direction = "CLOSER is Better" if dist_coef < 0 else "FARTHER is Better"
                print(f"Dist Result:  SIGNIFICANT ({direction})")
            else:
                print(f"Dist Result:  NOT Significant")
                
        except Exception as e:
            print(f"Error analyzing {metric_name}: {e}")

if __name__ == "__main__":
    main()
