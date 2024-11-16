
import asyncio
import os
import json
from pyppeteer import launch
from send_job_links import app

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

    await page.waitForSelector(
        'div[class ="jobs-search-discovery-tabs__pagination-arrows jobs-search-discovery-tabs__pagination-right-arrow"]'
    )
    await page.click(
        'div[class ="jobs-search-discovery-tabs__pagination-arrows jobs-search-discovery-tabs__pagination-right-arrow"]'
    )


async def remove_message_box(page):
    # Fixed to wait for a specific button and then click it
    await page.waitForSelector('button[class="msg-overlay-bubble-header__badge-container"]')
    await page.click('button[class="msg-overlay-bubble-header__badge-container"]')


async def go_to_easy_apply(page):
    # Keep clicking the SVG element until the desired image is found
    while True:
        # Click the SVG chevron-right icon
        await page.waitForSelector('svg[data-test-icon="chevron-right-small"]')
        await page.click('svg[data-test-icon="chevron-right-small"]')
        await page.screenshot()

        try:
            # Try to find the easy apply tab  by its src attribute
            target_img = await page.waitForSelector(
                'img[src="https://media.licdn.com/media/AAYAAgQJAAgAAQAAAAAAAGP4rUyqs0gcQHyq-AxUoT9SVg.png"]',
                timeout=2000)

            if target_img:
                # Click the tab if visible
                await target_img.click()
                break  # Exit the loop when the tab is visible and clicked

        except Exception:
            # If the tab is not found, continue clicking the next arrow
            pass


async def extract_page_info(page):
    # Wait for the pagination element to be present
    await page.waitForSelector('p.jobs-search-pagination__page-state')

    # Extract the text content inside the <p> tag
    page_info = await page.evaluate('''() => {
        return document.querySelector('p.jobs-search-pagination__page-state').innerText;
    }''')

    return str(page_info.strip()).split(" ")


# async def click_next_page(page):
#     # Scroll to the bottom of the page to load more content
#     # await page.evaluate('''() => {
#     #     window.scrollTo(0, document.body.scrollHeight);
#     # }''')
#
#
#     # Scroll down within the specific element containing the job listings
#     await page.evaluate('''() => {
#         const element = document.querySelector('.jobs-search-results-list');
#         element.scrollTop = element.scrollHeight; // Scroll to the bottom of the element
#     }''')
#
#
#     await asyncio.sleep(3)
#
#
#     # Wait for the next button to appear
#     try:
#         await page.waitForSelector('button[aria-label="View next page"]', timeout=5000) # Timeout after 5 seconds
#         await page.click('button[aria-label="View next page"]')
#     except Exception as e:
#         print(f"Error while clicking next page: {e}")
#
# async def job_pagination(page):
#     page_number_text = await extract_page_info(page)
#     current_page, last_page = int(page_number_text[1]), int(page_number_text[3])
#     print(current_page, last_page, (current_page + last_page))
#
#     while True:
#         # Use page.evaluate to extract all <li> elements within the specified <ul>
#         li_elements = await page.evaluate('''() => {
#             const liList = Array.from(document.querySelectorAll('ul.scaffold-layout__list-container li'));
#             return liList.map(li => li.outerHTML); // or return li.innerText to get text content
#         }''')
#
#         print('--------------', current_page, "---------", last_page)
#         await asyncio.sleep(2)
#
#         await click_next_page(page)
#
#         pass


# Explicitly handle the event loop, especially for Python 3.8+


async def click_next_page(page):
    try:
        # Scroll down within the specific element containing the job listings
        await page.evaluate('''() => {
            const element = document.querySelector('.jobs-search-results-list');
            element.scrollTop = element.scrollHeight; // Scroll to the bottom of the element
        }''')

        await asyncio.sleep(3)  # Wait for content to load

        # Try to click the "next page" button if it exists
        await page.waitForSelector('button[aria-label="View next page"]', timeout=5000)
        await page.click('button[aria-label="View next page"]')

        # Wait for the new content to load after clicking (adjust timeout as needed)
        await page.waitForNavigation(timeout=5000)  # Optional, in case of page reload or content update
    except Exception as e:
        print(f"Error or no more pages: {e}")
        return False  # No more pages to click
    return True  # Click was successful, there are more pages

# async def job_pagination(page):
#     # Initial page number extraction if necessary
#     page_number_text = await extract_page_info(page)
#     current_page, last_page = int(page_number_text[1]), int(page_number_text[3])
#     print(current_page, last_page)
#
#     # Loop through pages until no more "next page" button is found
#     while True:
#         # Extract and process the job listings on the current page
#         li_elements = await page.evaluate('''() => {
#             const liList = Array.from(document.querySelectorAll('ul.scaffold-layout__list-container li'));
#             return liList.map(li => li.outerHTML); // or return li.innerText for text content
#         }''')
#
#         # Process the extracted elements (e.g., print or store them)
#         print(f"Found {len(li_elements)} listings on page {current_page}")
#
#         # Click the "next page" button, exit the loop if there are no more pages
#         clicked = await click_next_page(page)
#         if not clicked:
#             print("No more pages to click, exiting loop.")
#             break  # Exit loop when no more pages are found
#
#         # Optionally extract page number info again if you want to track it
#         await asyncio.sleep(2)
#         current_page += 1  # Update page number manually if necessary
#         print(f"Moving to page {current_page}")
#

async def job_pagination(page):
    # Initial page number extraction if necessary
    page_number_text = await extract_page_info(page)
    current_page, last_page = int(page_number_text[1]), int(page_number_text[3])
    print(current_page, last_page)

    # Loop through pages until no more "next page" button is found
    while True:
        # Extract the href attribute of all <a> tags within the target container
        job_links = await page.evaluate('''() => {
            const aTags = Array.from(document.querySelectorAll('ul.scaffold-layout__list-container li a.job-card-container__link'));
            return aTags.map(a => a.href);
        }''')

        # Print the number of links found on the current page
        print(f"Found {len(job_links)} job links on page {current_page}")

        # Call send_links_to_microservice with the extracted links
        await app.send_links_to_microservice(job_links)
        # Click the "next page" button, exit the loop if there are no more pages
        clicked = await click_next_page(page)
        if not clicked:
            print("No more pages to click, exiting loop.")
            break  # Exit loop when no more pages are found

        # Optionally extract page number info again if you want to track it
        await asyncio.sleep(2)
        current_page += 1  # Update page number manually if necessary
        print(f"Moving to page {current_page}")

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(linkedin_controller())
    except RuntimeError as e:
        if str(e) == "Event loop is closed":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(linkedin_controller())
