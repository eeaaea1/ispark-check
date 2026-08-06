import os
import json
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://ispark.istanbul/abone/"


def telegram_gonder(mesaj):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mesaj
        },
        timeout=20
    )


print("İSPARK sitesi açılıyor...")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    print("Sayfa açıldı.")
        print("Otopark verisi isteniyor...")

    response = page.wait_for_response(
        lambda r: "getparks.php" in r.url,
        timeout=30000
    )

    page.select_option('select[name="AracTipi"]', value="1")
    page.select_option('select[name="YakitTipi"]', value="2")

    page.wait_for_timeout(3000)

    data = response.json()

    print(f"{len(data)} adet otopark bulundu.")

    park_1420 = None

    for park in data:
        if park.get("LocCode") == "1420":
            park_1420 = park
            break

    if park_1420 is None:
        print("1420 numaralı otopark bulunamadı.")
        browser.close()
        exit()

    print("1420 bulundu:")
    print(json.dumps(park_1420, indent=2, ensure_ascii=False))
    mesaj = (
        "✅ İSPARK KONTROL\n\n"
        f"Otopark: {park_1420['LocName']}\n"
        f"Kod: {park_1420['LocCode']}"
    )

    telegram_gonder(mesaj)

    print("Telegram bildirimi gönderildi.")

    browser.close()

print("İşlem tamamlandı.")
