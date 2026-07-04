from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto("https://ispark.istanbul/abone/")

    page.wait_for_timeout(5000)

    page.screenshot(path="ispark.png", full_page=True)

    browser.close()
