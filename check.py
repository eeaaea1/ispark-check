from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto("https://ispark.istanbul/abone/", wait_until="networkidle")

    print("İSPARK sayfası başarıyla açıldı.")

    browser.close()
