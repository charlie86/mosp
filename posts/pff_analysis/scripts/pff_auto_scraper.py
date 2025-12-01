import asyncio
import os
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError

# --- Configuration ---
START_WEEK = 1
END_WEEK = 12 # Set to 18 or current week as needed
SEASON = 2025
OUTPUT_FILE = "pff_run_blocking_data_2025_by_game.csv"
# Resolve paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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

async def scrape_team_game(page, week, team):
    """Scrapes data for a specific team and week."""
    url = f"https://premium.pff.com/nfl/games/{SEASON}/{week}/{team}/offense-run-blocking"
    print(f"Scraping {team} Week {week}: {url}")
    
    try:
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        if "404" in await page.title() or "Page Not Found" in await page.content():
            print(f"  -> Page not found")
            return []

        # New Strategy: Index Matching
        # The table is split. We collect players and grades separately and zip them.
        
        # 1. Find all player names
        # We filter for valid player links to avoid headers like "By Player"
        player_elements = await page.locator("a[href*='/nfl/players/']").all()
        players = []
        for p in player_elements:
            name = await p.inner_text()
            if "By Player" not in name:
                players.append(name)
        
        print(f"  -> Found {len(players)} players.")
        
        # 2. Find all grade badges
        # The class is .kyber-grade-badge__info-text
        grade_elements = await page.locator(".kyber-grade-badge__info-text").all()
        grades = []
        for g in grade_elements:
            grades.append(await g.inner_text())
            
        print(f"  -> Found {len(grades)} grades.")
        
        # 3. Zip them
        game_data = []
        # Assume 3 grades per player (Run Blocking is usually the first one based on verification)
        if len(grades) == 3 * len(players):
            for i in range(len(players)):
                # Run Blocking Grade is the first of the triplet (index 0, 3, 6...)
                rblk_grade = grades[i*3]
                
                game_data.append({
                    "Week": week,
                    "Team": team,
                    "Player": players[i].strip(),
                    "Grade": rblk_grade.strip()
                })
        elif len(players) == len(grades):
             # Fallback if only 1 grade is shown (unlikely but possible)
             for i in range(len(players)):
                game_data.append({
                    "Week": week,
                    "Team": team,
                    "Player": players[i].strip(),
                    "Grade": grades[i].strip()
                })
        else:
            print(f"  -> Mismatch! Players: {len(players)}, Grades: {len(grades)}")
            # Fallback: Try to map as many as possible
            limit = min(len(players), len(grades) // 3)
            for i in range(limit):
                rblk_grade = grades[i*3]
                game_data.append({
                    "Week": week,
                    "Team": team,
                    "Player": players[i].strip(),
                    "Grade": rblk_grade.strip()
                })
                
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
        
        for week in range(START_WEEK, END_WEEK + 1):
            print(f"=== Starting Week {week} ===")
            for team in TEAMS:
                team_data = await scrape_team_game(page, week, team)
                all_data.extend(team_data)
                
                # Save incrementally
                if all_data:
                    df = pd.DataFrame(all_data)
                    df.to_csv(OUTPUT_FILE, index=False)
            
            print(f"=== Completed Week {week} ===")

        print(f"Done. Saved to {OUTPUT_FILE}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
