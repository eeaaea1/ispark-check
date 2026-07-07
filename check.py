import os
import requests

# İSPARK API
url = "https://ispark.istanbul/abone/getparks.php"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://ispark.istanbul",
    "Referer": "https://ispark.istanbul/abone/"
}

# TEST İÇİN (Motosiklet + Benzin)
# Gerçek kullanıma geçince bunları 1 ve 2 yapacağız.
data = {
    "AracTipi": "1",
    "YakitTipi": "2"
}

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

print("İSPARK sorgulanıyor...")

response = requests.post(url, headers=headers, data=data)

print("HTTP:", response.status_code)

parks = response.json()

bulundu = False

for park in parks:
    if park["LocCode"] == "1420":
        bulundu = True

        print("1420 bulundu.")
        print(park)

        mesaj = (
            "✅ ISPARK UYARI\n\n"
            f"{park['LocName']}\n\n"
            "Test başarılı."
        )

        telegram = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": mesaj
            }
        )

        print("Telegram HTTP:", telegram.status_code)
        print("Telegram cevabı:")
        print(telegram.text)

        break

if not bulundu:
    print("1420 bulunamadı.")
