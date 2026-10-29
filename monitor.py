import os
import time
import requests
from playwright.sync_api import sync_playwright

TARGET = os.getenv("TARGET_PARKING", "1420 Harmantepe Zemin altı otopark")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram env yok:", message)
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, data=payload, timeout=20)
        print("Telegram status:", r.status_code)
    except Exception as e:
        print("Telegram error:", e)

def pick_first_select_option(page, index):
    try:
        selects = page.locator("select")
        count = selects.count()
        if count > index:
            sel = selects.nth(index)
            options = sel.locator("option")
            if options.count() > 1:
                sel.select_option(index=1)
                return True
    except Exception:
        pass
    return False

def check_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1200})
        page.goto("https://ispark.istanbul/abone/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)

        # Bu kısım siteye göre değişebilir
        # Dropdown varsa, ilk 2 select alanına örnek değer ver
        pick_first_select_option(page, 0)
        time.sleep(1)
        pick_first_select_option(page, 1)
        time.sleep(2)

        full_text = page.locator("body").inner_text()
        print("BODY text first 2000 chars:")
        print(full_text[:2000])

        if TARGET.lower() in full_text.lower():
            msg = f"✅ EŞLEŞME BULUNDU: {TARGET}"
            print(msg)
            send_telegram(msg)
        else:
            msg = f"❌ Hedef bulunamadı: {TARGET}\nSayfa texti tarandı ama eşleşme yok."
            print(msg)
            # İstersen bunun Telegram gönderimini kapatabilirsin.
            # send_telegram(msg)

        browser.close()

if __name__ == "__main__":
    check_site()
