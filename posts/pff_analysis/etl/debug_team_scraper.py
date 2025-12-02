import asyncio
import os
from playwright.async_api import async_playwright

# Configuration
AUTH_FILE = "/Users/charliethompson/Documents/mosp/shhhh/pff_auth.json"
URL = "https://premium.pff.com/nfl/teams/2024/REGPO"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=AUTH_FILE)
        page = await context.new_page()
        
        print(f"Navigating to {URL}...")
        await page.goto(URL, wait_until='networkidle')
        
        # Wait for table
        await page.wait_for_selector(".kyber-table-body__row", timeout=15000)
        
        # Get first stats row (assuming it's the second set of rows)
        rows = await page.locator(".kyber-table-body__row").all()
        
        # Find a row that looks like a stats row (not just a name)
        for i, row in enumerate(rows):
            text = await row.inner_text()
            print(f"Row {i} Text: {text}")
            if "Team Reports" in text:
                print(f"Found Stats Row at index {i}")
                # Print HTML
                html = await row.inner_html()
                print(f"Row HTML:\n{html}")
                with open("team_row_debug.html", "w") as f:
                    f.write(html)
                print("Saved HTML to team_row_debug.html")
                break
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
