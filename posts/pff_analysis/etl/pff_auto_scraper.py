import asyncio
import os
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError

# --- Configuration ---
START_WEEK = 1
END_WEEK = 22 # Covers Regular Season (1-18) and Playoffs (19-22)
SEASONS = [2020, 2021, 2022, 2023, 2024, 2025]
# Resolve paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, '../data/pff_run_blocking_data_multi_season.csv')
# Go up 3 levels: scripts -> pff_analysis -> posts -> root
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
AUTH_FILE = os.path.join(PROJECT_ROOT, "shhhh/pff_auth.json")

# List of team slugs for URL construction
TEAMS = [
    "arizona-cardinals", "atlanta-falcons", "baltimore-ravens", "buffalo-bills",
    "carolina-panthers", "chicago-bears", "cincinnati-bengals", "cleveland-browns",
    "dallas-cowboys", "denver-broncos", "detroit-lions", "green-bay-packers",
    "houston-texans", "indianapolis-colts", "jacksonville-jaguars", "kansas-city-chiefs",
    "las-vegas-raiders", "los-angeles-chargers", "los-angeles-rams", "miami-dolphins",
    "minnesota-vikings", "new-england-patriots", "new-orleans-saints", "new-york-giants",
    "new-york-jets", "philadelphia-eagles", "pittsburgh-steelers", "san-francisco-49ers",
    "seattle-seahawks", "tampa-bay-buccaneers", "tennessee-titans", "washington-commanders"
]

async def login_and_save_state(page):
    """Handles the login process and saves the storage state."""
    print("Navigate to login page...")
    await page.goto("https://premium.pff.com/login")
    
    print("Please log in manually in the browser window.")
    print("Waiting for you to be redirected...")
    
    try:
        await page.wait_for_url("**/nfl/**", timeout=300000) # 5 minutes
        print("Login detected!")
        await page.context.storage_state(path=AUTH_FILE)
        print(f"Authentication state saved to {AUTH_FILE}")
    except TimeoutError:
        print("Login timed out.")
        return False
    return True

async def scrape_team_game(page, season, week, team):
    """Scrapes data for a specific team, season, and week."""
    url = f"https://premium.pff.com/nfl/games/{season}/{week}/{team}/offense-run-blocking"
    print(f"Scraping {season} Week {week} {team}: {url}")
    
    try:
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        if "404" in await page.title() or "Page Not Found" in await page.content():
            return []

        # Strategy: Split Table Extraction
        # The table has fixed columns (Names) and scrollable columns (Stats).
        # We separate rows based on whether they contain a player link.
        
        rows = await page.locator(".kyber-table-body__row").all()
        
        name_rows = []
        stat_rows = []
        
        for row in rows:
            if await row.locator("a[href*='/nfl/players/']").count() > 0:
                name_rows.append(row)
            else:
                stat_rows.append(row)
        
        # Validation: Stat rows usually have 2 extra rows (header/footer padding)
        # We expect stat_rows[1] to match name_rows[0]
        
        game_data = []
        
        # Zip name_rows with stat_rows offset by 1
        # We limit to len(name_rows) to avoid index errors
        for i in range(len(name_rows)):
            try:
                # 1. Player Name
                name_row = name_rows[i]
                player_name = await name_row.locator("a[href*='/nfl/players/']").inner_text()
                
                # 2. Position & Grade from Stat Row
                if i + 1 < len(stat_rows):
                    stat_row = stat_rows[i+1]
                    
                    # Position is the first line of text in the stat row
                    row_text = await stat_row.inner_text()
                    position = row_text.split('\n')[0].strip() if row_text else "Unknown"
                    
                    # Grade
                    # Run Blocking Grade is usually the first grade badge in the row
                    grades = await stat_row.locator(".kyber-grade-badge__info-text").all()
                    rblk_grade = await grades[0].inner_text() if grades else ""
                else:
                    print(f"  -> Warning: Missing stat row for {player_name}")
                    position = "Unknown"
                    rblk_grade = ""

                if player_name and rblk_grade:
                    game_data.append({
                        "Season": season,
                        "Week": week,
                        "Team": team,
                        "Player": player_name.strip(),
                        "Position": position,
                        "Grade": rblk_grade.strip()
                    })
            except Exception as row_e:
                # print(f"    -> Error parsing row {i}: {row_e}")
                continue

        return game_data

    except Exception as e:
        print(f"  -> Error: {e}")
        return []

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        if os.path.exists(AUTH_FILE):
            print(f"Loading auth state from {AUTH_FILE}")
            context = await browser.new_context(storage_state=AUTH_FILE)
        else:
            print("No auth state found. Creating new context.")
            context = await browser.new_context()
            
        page = await context.new_page()
        
        # Check login
        await page.goto("https://premium.pff.com/nfl/grades/blocking/run") # Go to a protected page
        await page.wait_for_timeout(2000)
        
        if "login" in page.url or await page.locator("text=Sign In").count() > 0:
            if not await login_and_save_state(page):
                await browser.close()
                return

        all_data = []
        processed_keys = set()

        if os.path.exists(OUTPUT_FILE):
            print(f"Loading existing data from {OUTPUT_FILE} to identify processed items...")
            existing_df = pd.read_csv(OUTPUT_FILE)
            existing_df['Week'] = existing_df['Week'].astype(str)        # Create a set of processed (Season, Week, Team) to skip
            processed_keys = set()
            for row in existing_df.to_dict(orient='records'):
                # Normalize week to string to handle both '1' and 'WC'
                processed_keys.add((int(row['Season']), str(row['Week']), row['Team']))
            all_data = existing_df.to_dict(orient='records') # Re-load existing data into all_data
            print(f"Loaded {len(processed_keys)} previously processed items.")
        
        # Define weeks: 1-18 for regular season, plus playoff codes
        # 2020 had 17 weeks, but iterating to 18 is fine (will 404/skip).
        # Playoff codes: WC (Wild Card), DP (Divisional), CC (Conf. Champ), SB (Super Bowl)
        WEEKS = list(range(1, 19)) + ["WC", "DP", "CC", "SB"]
        
        for season in SEASONS:
            print(f"=== Starting Season {season} ===")
            for week in WEEKS:
                print(f"  --- Week {week} ---")
                for team in TEAMS:
                    # Check if already processed
                    # Note: Week in CSV might be string for codes, int for numbers.
                    # We need to handle type matching for the check.
                    
                    # Normalize week to string for comparison if needed, or check both
                    # In CSV, 'WC' is string, '1' is int or string '1'.
                    # Let's check against string representation to be safe.
                    
                    # Create a key for the current item
                    current_key = (season, str(week), team)
                    
                    # Check against processed keys (which we should normalize to string week)
                    if current_key in processed_keys:
                        # print(f"Skipping {season} Week {week} {team} (Already scraped)")
                        continue
                        
                    team_data = await scrape_team_game(page, season, week, team)
                    if team_data:
                        all_data.extend(team_data)
                        # Add the current key to processed_keys to avoid re-scraping if saving fails later
                        processed_keys.add(current_key)
                    
                    # Save incrementally
                    if all_data:
                        df = pd.DataFrame(all_data)
                        df.to_csv(OUTPUT_FILE, index=False)
                
                print(f"  --- Completed Week {week} ---")
            print(f"=== Completed Season {season} ===")

        print(f"Done. Saved to {OUTPUT_FILE}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
