from playwright.sync_api import sync_playwright

print("Program başladı")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page(
        viewport={"width": 1400, "height": 2500}
    )

    page.goto(
        "https://ispark.istanbul/abone/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    page.screenshot(
        path="ispark.png",
        full_page=True
    )

    print("Ekran görüntüsü oluşturuldu")

    browser.close()

print("Program bitti")
