import os
import json
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://ispark.istanbul/abone/"


def telegram_gonder(mesaj):
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mesaj
        },
        timeout=20
    )

    print("Telegram HTTP:", response.status_code)


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

    page.wait_for_timeout(5000)

    print("Araç tipi seçiliyor...")

    try:
        page.select_option(
            'select[name="AracTipi"]',
            value="1"
        )
        print("Araç tipi seçildi.")
    except Exception as e:
        print("Araç tipi seçilemedi:", e)

    print("Yakıt tipi seçiliyor...")

    try:
        page.select_option(
            'select[name="YakitTipi"]',
            value="2"
        )
        print("Yakıt tipi seçildi.")
    except Exception as e:
        print("Yakıt tipi seçilemedi:", e)

    print("getparks.php isteği bekleniyor...")

    try:
        with page.expect_response(
            lambda r: "getparks.php" in r.url,
            timeout=30000
        ) as response_info:

            page.wait_for_timeout(1000)

        response = response_info.value

        print("getparks.php bulundu.")
        print("URL:", response.url)
        print("HTTP:", response.status)

    except Exception as e:

        print("getparks.php isteği yakalanamadı.")
        print("HATA:", e)

        browser.close()
        exit(1)

    try:

        data = response.json()

    except Exception as e:

        print("JSON okunamadı.")
        print("HATA:", e)
        print("Gelen cevap:")
        print(response.text())

        browser.close()
        exit(1)

    print("JSON başarıyla alındı.")

    if isinstance(data, dict):

        print("JSON bir liste değil, sözlük olarak geldi.")

        if "data" in data:
            data = data["data"]

        elif "parks" in data:
            data = data["parks"]

        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
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
        exit(0)

    print("1420 NUMARALI OTOPARK BULUNDU!")

    print(
        json.dumps(
            park_1420,
            indent=2,
            ensure_ascii=False
        )
    )

    loc_name = park_1420.get(
        "LocName",
        "Bilinmiyor"
    )

    loc_code = park_1420.get(
        "LocCode",
        "1420"
    )

    mesaj = (
        "✅ İSPARK KONTROL\n\n"
        f"Otopark: {loc_name}\n"
        f"Kod: {loc_code}"
    )

    telegram_gonder(mesaj)

    print("Telegram bildirimi gönderildi.")

    browser.close()

print("İşlem tamamlandı.")
