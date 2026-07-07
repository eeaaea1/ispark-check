import requests

URL = "https://ispark.istanbul/abone/getparks.php"

data = {
    "AracTipi": "10",   # Test için Motosiklet
    "YakitTipi": "1"    # Test için Benzin
}

print("İSPARK sorgulanıyor...")

response = requests.post(URL, data=data)

print("HTTP Durumu:", response.status_code)

text = response.text

if "1420" in text or "Harmantepe" in text:
    print("✅ 1420 BULUNDU")
    raise Exception("TEST BAŞARILI - 1420 bulundu")
else:
    print("❌ 1420 bulunamadı")
