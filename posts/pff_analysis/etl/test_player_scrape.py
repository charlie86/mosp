import asyncio
import os
from playwright.async_api import async_playwright

AUTH_FILE = "/Users/charliethompson/Documents/mosp/shhhh/pff_auth.json"
URL = "https://premium.pff.com/nfl/positions/2024/SINGLE/offense-blocking?position=G,T,C"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=AUTH_FILE)
        page = await context.new_page()
        
        print(f"Navigating to {URL}...")
        await page.goto(URL, wait_until='networkidle')
        
        try:
            await page.wait_for_selector(".kyber-table-body__row", timeout=10000)
            print("Table found!")
            
            # Check for locks
            content = await page.content()
            if "kyber-svg-lock-solid" in content:
                print("LOCKED CONTENT DETECTED!")
            else:
                print("Content appears unlocked.")
                
        except:
            print("Table not found.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
