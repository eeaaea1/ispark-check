import os
import requests

url = "https://ispark.istanbul/abone/getparks.php"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://ispark.istanbul",
    "Referer": "https://ispark.istanbul/abone/"
}

# TEST İÇİN
data = {
    "AracTipi": "10",   # Motosiklet
    "YakitTipi": "1"    # Benzin
}

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

r = requests.post(url, headers=headers, data=data)
parks = r.json()

bulundu = False

for park in parks:
    if park["LocCode"] == "1420":
        bulundu = True

        mesaj = (
            "✅ ISPARK UYARI\n\n"
            f"{park['LocName']}\n\n"
            "Test başarılı."
        )

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": mesaj
            }
        )

        print("Telegram mesajı gönderildi.")
        break

if not bulundu:
    print("1420 bulunamadı.")
