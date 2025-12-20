import asyncio
import os
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError
from google.cloud import bigquery
from oauth2client.service_account import ServiceAccountCredentials

# --- Configuration ---
START_SEASON = 2006
END_SEASON = 2025
START_WEEK = 1

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
AUTH_FILE = os.path.join(PROJECT_ROOT, "shhhh/pff_auth.json")

# BigQuery Config
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
DATASET_ID = 'pff_analysis'
TABLE_ID = 'position_stats'

def get_bq_client():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found.")
        return None
    try:
        return bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    except Exception as e:
        print(f"BQ Auth failed: {e}")
        return None

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

async def scrape_week(page, season, week):
    url = f"https://premium.pff.com/nfl/positions/{season}/SINGLE/offense-blocking?week={week}"
    print(f"Scraping {season} Week {week}: {url}")
    
    # Retry logic for navigation
    for attempt in range(3):
        try:
            await page.goto(url, timeout=60000) # 60s timeout
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
        
        # Try to set rows per page to 200
        try:
            rows_200 = page.locator(".kyber-table-pagination__rows-select label:has-text('200')")
            if await rows_200.count() > 0:
                if "active" not in await rows_200.get_attribute("class"):
                    # print("  -> Setting rows per page to 200...")
                    await rows_200.click()
                    await page.wait_for_timeout(3000)
        except Exception:
            pass

        week_data = []
        page_num = 1
        
        while True:
            # print(f"  -> Processing Page {page_num}...")
            rows = await page.locator(".kyber-table-body__row").all()
            
            name_rows = []
            stat_rows = []
            
            for row in rows:
                if await row.locator("a[href*='/nfl/players/']").count() > 0:
                    name_rows.append(row)
                else:
                    text = await row.inner_text()
                    if text.strip():
                        stat_rows.append(row)
            
            for i in range(min(len(name_rows), len(stat_rows))):
                try:
                    name_row = name_rows[i]
                    name_text = await name_row.inner_text()
                    parts = name_text.split('\n')
                    rank = parts[0].strip() if len(parts) > 0 else ""
                    player_name = parts[1].strip() if len(parts) > 1 else ""
                    
                    stat_row = stat_rows[i]
                    stat_text = await stat_row.inner_text()
                    stats = stat_text.split('\n')
                    
                    if len(stats) < 12:
                        continue
                        
                    position = stats[1].strip()
                    team = stats[3].strip()
                    snap_counts_block = stats[5].strip()
                    snap_counts_run_block = stats[7].strip()
                    snap_counts_pass_block = stats[8].strip()
                    grade_offense = stats[9].strip()
                    grade_run_block = stats[10].strip()
                    grade_pass_block = stats[11].strip()
                    
                    week_data.append({
                        "Season": season,
                        "Week": week,
                        "Rank": rank,
                        "Player": player_name,
                        "Team": team,
                        "Position": position,
                        "SnapCount_Block": snap_counts_block,
                        "SnapCount_RunBlock": snap_counts_run_block,
                        "SnapCount_PassBlock": snap_counts_pass_block,
                        "Grade_Offense": grade_offense,
                        "Grade_RunBlock": grade_run_block,
                        "Grade_PassBlock": grade_pass_block
                    })
                    
                except Exception:
                    continue
            
            next_btn = page.locator("button.kyber-table-pagination__button-next")
            if await next_btn.count() > 0:
                is_disabled = await next_btn.is_disabled()
                if not is_disabled:
                    await next_btn.click()
                    await page.wait_for_timeout(3000)
                    page_num += 1
                else:
                    break
            else:
                break
                
        return week_data

    except Exception as e:
        print(f"  -> Error scraping week: {e}")
        return []

async def main():
    async with async_playwright() as p:
        # BigQuery Setup
        print("Setting up BigQuery connection...")
        bq_client = get_bq_client()
        if not bq_client:
            return

        existing_weeks = set()
        table_ref = f"{bq_client.project}.{DATASET_ID}.{TABLE_ID}"
        
        try:
            print(f"Checking existing data in {table_ref}...")
            query = f"SELECT Season, Week FROM `{table_ref}` GROUP BY 1, 2"
            query_job = bq_client.query(query)
            try:
                results = query_job.result()
                for row in results:
                    existing_weeks.add((row.Season, row.Week))
                print(f"  Identified {len(existing_weeks)} unique Season/Week combos already scraped.")
            except Exception as e:
                # Table might not exist yet if only just setup, or empty
                print(f"  Error querying (table might be empty/missing): {e}")

        except Exception as e:
            print(f"  BQ setup check failed: {e}")
            # Do not return, might just be empty table. Continue.

        # Browser Setup
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
        await page.goto("https://premium.pff.com/nfl/grades/blocking/run")
        await page.wait_for_timeout(2000)
        if "login" in page.url or await page.locator("text=Sign In").count() > 0 or await page.locator("text=Unlock PFF+").count() > 0:
             if not await login_and_save_state(page):
                await browser.close()
                return

        # Generate list of (Season, Week) tuples to scrape
        tasks = []
        full_weeks = list(range(1, 19)) + [28, 29, 30, 32]
        
        for s in range(START_SEASON, END_SEASON + 1):
            for w in full_weeks:
                # Filter if we already have it!
                if (s, w) not in existing_weeks:
                    tasks.append((s, w))
                
        print(f"Starting scrape. Weeks remaining: {len(tasks)}")
        
        for season, week in tasks:
            data = await scrape_week(page, season, week)
            if data:
                # Prepare for BQ Streaming
                # Ensure types are correct, BQ streaming is picky about types relative to JSON
                rows_to_insert = []
                for row in data:
                    # Basic cleaning
                    cleaned_row = row.copy()
                    # Integers
                    for col in ['Season', 'Week', 'SnapCount_Block', 'SnapCount_RunBlock', 'SnapCount_PassBlock']:
                        try:
                            cleaned_row[col] = int(cleaned_row[col])
                        except:
                            cleaned_row[col] = 0
                            
                    # Floats
                    for col in ['Grade_Offense', 'Grade_RunBlock', 'Grade_PassBlock']:
                        try:
                            cleaned_row[col] = float(cleaned_row[col])
                        except:
                            cleaned_row[col] = 0.0
                            
                    rows_to_insert.append(cleaned_row)
                
                # Write to BigQuery
                try:
                    errors = bq_client.insert_rows_json(table_ref, rows_to_insert)
                    if errors == []:
                        print(f"  -> Saved {len(data)} records for {season} Week {week}")
                    else:
                        print(f"  -> Errors inserting rows: {errors}")
                except Exception as e:
                     print(f"  -> Error inserting to BQ: {e}")

            else:
                print(f"  -> No data for {season} Week {week}")
            
        print(f"Done! Scrape complete.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
