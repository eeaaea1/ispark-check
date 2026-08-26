import requests

URL = "https://ispark.istanbul/abone/"

print("İSPARK bağlantı testi başlıyor...")

try:
    r = requests.get(
        URL,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    print("HTTP DURUMU:", r.status_code)
    print("CEVAP UZUNLUĞU:", len(r.text))
    print("İLK 500 KARAKTER:")
    print(r.text[:500])

except Exception as e:
    print("BAĞLANTI HATASI:")
    print(repr(e))
    raise
