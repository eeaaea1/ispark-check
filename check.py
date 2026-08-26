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

    print("Sayfa açılıyor...")

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Sayfa açıldı.")

    # Sayfanın yüklenmesini bekle
    page.wait_for_timeout(5000)

    print("Otopark verisi aranıyor...")

    # getparks.php isteklerini kontrol et
    response = None

    try:
        response = page.wait_for_response(
            lambda r: "getparks.php" in r.url,
            timeout=10000
        )
    except Exception:
        print("Sayfa açılırken getparks.php yakalanamadı.")

    # Araç tipi
    try:
        page.select_option(
            'select[name="AracTipi"]',
            value="1"
        )
        print("Araç tipi seçildi.")
    except Exception as e:
        print("Araç tipi seçilemedi:", e)

    # Yakıt tipi
    try:
        page.select_option(
            'select[name="YakitTipi"]',
            value="2"
        )
        print("Yakıt tipi seçildi.")
    except Exception as e:
        print("Yakıt tipi seçilemedi:", e)

    # AJAX isteğinin oluşması için bekle
    page.wait_for_timeout(5000)

    # Yeni getparks.php isteğini yakala
    if response is None:
        try:
            response = page.wait_for_response(
                lambda r: "getparks.php" in r.url,
                timeout=30000
            )
        except Exception as e:
            print("getparks.php isteği bulunamadı.")
            print(e)
            browser.close()
            exit(1)

    print("getparks.php bulundu.")
    print("URL:", response.url)

    try:
        data = response.json()
    except Exception as e:
        print("JSON okunamadı.")
        print(e)
        print(response.text())
        browser.close()
        exit(1)

    print(f"{len(data)} adet otopark bulundu.")

    park_1420 = None

    for park in data:
        if str(park.get("LocCode")) == "1420":
            park_1420 = park
            break

    if park_1420 is None:
        print("1420 numaralı otopark bulunamadı.")
        browser.close()
        exit()

    print("1420 bulundu:")

    print(
        json.dumps(
            park_1420,
            indent=2,
            ensure_ascii=False
        )
    )

    mesaj = (
        "✅ İSPARK KONTROL\n\n"
        f"Otopark: {park_1420.get('LocName', 'Bilinmiyor')}\n"
        f"Kod: {park_1420.get('LocCode', 'Bilinmiyor')}"
    )

    telegram_gonder(mesaj)

    print("Telegram bildirimi gönderildi.")

    browser.close()

print("İşlem tamamlandı.")
