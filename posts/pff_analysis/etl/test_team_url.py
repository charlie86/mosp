import asyncio
from playwright.async_api import async_playwright
import os

# Configuration
AUTH_FILE = "/Users/charliethompson/Documents/mosp/shhhh/pff_auth.json"
URL = "https://premium.pff.com/nfl/teams/2025/REGPO"

async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=AUTH_FILE)
        page = await context.new_page()
        
        print(f"Navigating to {URL}...")
        await page.goto(URL, wait_until='networkidle')
        
        print(f"Page Title: {await page.title()}")
        
        # Wait for table
        try:
            await page.wait_for_selector('.kyber-table-body__row', timeout=10000)
            print("Table found!")
        except:
            print("Table not found immediately. Saving screenshot...")
            await page.screenshot(path="team_page_debug.png")
            
        # Get headers
        headers = await page.locator('.kyber-table-header__row div').all_inner_texts()
        print("Headers:", headers)
        
        # Get first few rows
        rows = await page.locator('.kyber-table-body__row').all()
        print(f"Found {len(rows)} rows.")
        
        if rows:
            first_row = await rows[0].locator('td').all_inner_texts()
            print("First Row Data:", first_row)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
