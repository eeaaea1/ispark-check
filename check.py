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
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    page = browser.new_page()

    # Network kayıtları
    def request_log(request):
        if "ispark.istanbul" in request.url:
            print("REQUEST:", request.method, request.url)

    page.on("request", request_log)

    print("Sayfa açılıyor...")

    try:
        page.goto(
            URL,
            wait_until="commit",
            timeout=30000
        )

        print("İSPARK bağlantısı kuruldu.")

    except Exception as e:

        print("page.goto hatası:")
        print(e)

        try:
            page.screenshot(
                path="ispark_error.png",
                full_page=True
            )
            print("Hata ekran görüntüsü kaydedildi.")
        except Exception as screenshot_error:
            print("Ekran görüntüsü alınamadı:", screenshot_error)

        browser.close()
        raise

    # Sayfanın JavaScript'lerinin çalışması için bekle
    page.wait_for_timeout(10000)

    print("Sayfa URL:", page.url)
    print("Sayfa başlığı:", page.title())

    print("Otopark verisi aranıyor...")

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

    print("getparks.php isteği bekleniyor...")

    try:

        with page.expect_response(
            lambda r: "getparks.php" in r.url,
            timeout=30000
        ) as response_info:

            page.wait_for_timeout(1000)

        response = response_info.value

        print("getparks.php bulundu!")
        print("URL:", response.url)
        print("HTTP:", response.status)

    except Exception as e:

        print("getparks.php isteği yakalanamadı.")
        print("HATA:", e)

        try:
            page.screenshot(
                path="ispark_error.png",
                full_page=True
            )
            print("Ekran görüntüsü kaydedildi.")
        except Exception:
            pass

        browser.close()
        raise

    try:
        data = response.json()
    except Exception as e:
        print("JSON okunamadı:", e)
        print(response.text())
        browser.close()
        raise

    print("JSON başarıyla alındı.")

    if isinstance(data, dict):
        if "data" in data:
            data = data["data"]
        elif "parks" in data:
            data = data["parks"]

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

    mesaj = (
        "✅ İSPARK KONTROL\n\n"
        f"Otopark: {park_1420.get('LocName', 'Bilinmiyor')}\n"
        f"Kod: {park_1420.get('LocCode', '1420')}"
    )

    telegram_gonder(mesaj)

    print("Telegram bildirimi gönderildi.")

    browser.close()

print("İşlem tamamlandı.")
