from playwright.sync_api import sync_playwright

print("1- Program başladı")

with sync_playwright() as p:
    print("2- Playwright açıldı")

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("3- Sayfaya gidiliyor")

    page.goto("https://example.com")

    print("4- Sayfa açıldı")

    page.screenshot(path="ispark.png")

    print("5- Ekran görüntüsü alındı")

    browser.close()

print("6- Program bitti")
