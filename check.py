from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto("https://ispark.istanbul/abone/", wait_until="networkidle")

    page.screenshot(path="ispark.png", full_page=True)

    print("Ekran görüntüsü alındı.")

    browser.close()
