import asyncio
import os
from playwright.async_api import async_playwright

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
AUTH_FILE = os.path.join(PROJECT_ROOT, "shhhh/pff_auth.json")
URL = "https://premium.pff.com/nfl/positions/2025/SINGLE/offense-blocking?position=G,T,C&week=13"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=AUTH_FILE)
        page = await context.new_page()
        
        print(f"Navigating to {URL}...")
        await page.goto(URL)
        
        try:
            print("Waiting for table...")
            await page.wait_for_selector(".kyber-table-body__row", timeout=10000)
            
            # Look for pagination controls
            # Common classes: .kyber-pagination, .pagination, buttons with "Next" text
            print("\n--- Searching for Pagination ---")
            
            # 1. By Text
            next_buttons = await page.locator("button:has-text('Next')").all()
            print(f"Buttons with 'Next': {len(next_buttons)}")
            
            # 2. By Icon (often an arrow)
            # 3. By Class
            paginations = await page.locator("[class*='pagination']").all()
            print(f"Elements with 'pagination' class: {len(paginations)}")
            
            if paginations:
                print("Pagination HTML:")
                print(await paginations[0].inner_html())
                
            # Check for a dropdown that controls rows per page
            rows_per_page = await page.locator("[class*='rows-per-page']").all()
            print(f"Elements with 'rows-per-page' class: {len(rows_per_page)}")
            
            # Check if there is a "Load More" button
            load_more = await page.locator("button:has-text('Load More')").all()
            print(f"Buttons with 'Load More': {len(load_more)}")

        except Exception as e:
            print(f"Error: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
