
import asyncio
import time
import os
import json
from pyppeteer import launch

COOKIE_FILE = '../cookies.json'

async def save_cookies(page):
    cookies = await page.cookies()
    with open(COOKIE_FILE, 'w') as f:
        json.dump(cookies, f)
    print("Cookies saved!")

async def load_cookies(page):
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
        await page.setCookie(*cookies)
        print("Cookies loaded!")
        return True
    return False

async def check_if_logged_in(page):
    await page.goto("https://www.linkedin.com/feed/")  # Go to a page that only works if logged in
    await asyncio.sleep(3)  # Give time for page to load
    content = await page.content()
    if "Sign In" in content or "login" in page.url:
        print("Not logged in, need to log in manually.")
        return False
    print("Logged in successfully with cookies.")
    return True

async def linkedin_controller():
    # Launch the browser with headless mode off for debugging
    browser = await launch({"headless": False, "defaultViewport": None})

    try:
        page = await browser.newPage()

        # Try to load cookies first
        if await load_cookies(page):
            # Check if we are logged in
            if not await check_if_logged_in(page):
                await start_script(page)  # Perform manual login if cookies are invalid
                await save_cookies(page)  # Save new cookies after successful login
        else:
            # Perform manual login if no cookies are found
            await start_script(page)
            await save_cookies(page)

        # Proceed to the job section after successful login
        await go_to_jobs(page)

        await click_on_show_all(page)
        await page.screenshot()

        await go_to_easy_apply(page)
        await page.screenshot()

        await job_pagination(page)

        await asyncio.sleep(5)  # Adjust based on need

    finally:
        await browser.close()

async def start_script(page):
    await page.goto("https://www.linkedin.com/login/")
    await page.waitForSelector('#username')
    await page.type('#username', 'Emmanuelolaoye44@gmail.com', delay=120)

    await page.waitForSelector('#password')
    await page.type('#password', 'yeahboi12', delay=120)

    await page.click('button[type="submit"]')
    await asyncio.sleep(5)

async def go_to_jobs(page):
    await asyncio.sleep(2)
    await page.waitForSelector('li-icon[type="job"]')
    await asyncio.sleep(2)
    await page.click('li-icon[type="job"]')

async def click_on_show_all(page):
    await page.waitForSelector('a[aria-label="Show all Top job picks for you"]')
    await page.click('a[aria-label="Show all Top job picks for you"]')
    await page.screenshot()

async def go_to_easy_apply(page):
    # Simulating going to the easy apply section
    pass

async def job_pagination(page):
    # Pagination logic goes here
    pass

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(linkedin_controller())
    except RuntimeError as e:
        if str(e) == "Event loop is closed":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(linkedin_controller())
