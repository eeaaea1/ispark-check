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

data = {
    "AracTipi": "10",   # Test: Motosiklet
    "YakitTipi": "1"    # Test: Benzin
}

r = requests.post(url, headers=headers, data=data)
parks = r.json()

bulundu = False

for park in parks:
    if park["LocCode"] == "1420":
        bulundu = True
        print("BULUNDU!")
        print(park)
        break

if not bulundu:
    print("1420 bulunamadı.")
