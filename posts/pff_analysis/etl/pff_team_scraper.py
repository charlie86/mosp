import asyncio
import os
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError

# --- Configuration ---
START_SEASON = 2006
END_SEASON = 2025

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
AUTH_FILE = os.path.join(PROJECT_ROOT, "shhhh/pff_auth.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, '../data/pff_team_defense_data_2006_2025.csv')

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

async def scrape_season(page, season):
    url = f"https://premium.pff.com/nfl/teams/{season}/REGPO"
    print(f"Scraping {season}: {url}")
    
    # Retry logic for navigation
    for attempt in range(3):
        try:
            await page.goto(url, timeout=60000)
            break
        except TimeoutError:
            print(f"  -> Timeout on attempt {attempt+1}. Retrying...")
            if attempt == 2:
                print("  -> Failed to load page after 3 attempts.")
                return []
    
    try:
        # Wait for table
        await page.wait_for_selector(".kyber-table-body__row", timeout=15000)
        await page.wait_for_timeout(2000) # Ensure full render
        
        # Check for locks
        content = await page.content()
        if "kyber-svg-lock-solid" in content:
            print("  -> LOCKED CONTENT DETECTED! Refreshing...")
            await page.reload()
            await page.wait_for_timeout(5000)
            
        season_data = []
        rows = await page.locator(".kyber-table-body__row").all()
        
        name_rows = []
        stat_rows = []
        
        # Split rows into Name rows and Stat rows
        for row in rows:
            # Team rows usually have a link to the team page or an image
            # Checking for 'a' tag or specific class might work.
            # In position scraper: row.locator("a[href*='/nfl/players/']")
            # For teams: likely /nfl/teams/
            if await row.locator("a[href*='/nfl/teams/']").count() > 0:
                name_rows.append(row)
            else:
                stat_rows.append(row)
        
        print(f"  -> Found {len(name_rows)} name rows and {len(stat_rows)} stat rows.")
        
        # Match by index
        for i in range(min(len(name_rows), len(stat_rows))):
            try:
                name_row = name_rows[i]
                stat_row = stat_rows[i]
                
                # Extract Team Name
                name_text = await name_row.inner_text()
                # Name text might contain Rank\nTeamName
                parts_name = [p.strip() for p in name_text.split('\n') if p.strip()]
                
                team_name = "Unknown"
                # Usually the last part is the team name if rank is present
                # e.g. "1\nSan Francisco 49ers"
                if len(parts_name) > 0:
                    team_name = parts_name[-1]
                
                # Extract Stats
                stat_text = await stat_row.inner_text()
                parts_stat = [p.strip() for p in stat_text.split('\n') if p.strip()]
                
                # Combine
                # We want to preserve the raw parts for processing
                # But we explicitly want the Team Name now
                
                record = {
                    "Season": season,
                    "Team": team_name,
                    "RawStats": parts_stat
                }
                season_data.append(record)
                
            except Exception as e:
                print(f"  -> Error processing row {i}: {e}")
                continue
            
        return season_data

    except Exception as e:
        print(f"  -> Error scraping season {season}: {e}")
        return []

async def main():
    async with async_playwright() as p:
        # USE HEADLESS=FALSE as requested
        browser = await p.chromium.launch(headless=False)
        
        context = None
        if os.path.exists(AUTH_FILE):
            print(f"Loading auth state from {AUTH_FILE}")
            context = await browser.new_context(storage_state=AUTH_FILE)
        else:
            print("No auth state found. Creating new context.")
            context = await browser.new_context()
            
        page = await context.new_page()
        
        # Check login
        print("Checking login status...")
        await page.goto("https://premium.pff.com/nfl/teams/2024/REGPO")
        await page.wait_for_timeout(3000)
        
        # If we see "Sign In" or "Unlock", we need to login
        if await page.locator("text=Sign In").count() > 0 or await page.locator("text=Unlock PFF+").count() > 0:
             print("Login required.")
             if not await login_and_save_state(page):
                await browser.close()
                return
        else:
            print("Already logged in.")
        
        all_data = []
        
        for season in range(START_SEASON, END_SEASON + 1):
            data = await scrape_season(page, season)
            if data:
                all_data.extend(data)
                print(f"  -> Scraped {len(data)} rows for {season}")
            else:
                print(f"  -> No data for {season}")
                
        # Save raw data
        df = pd.DataFrame(all_data)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Saved raw team data to {OUTPUT_FILE}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
