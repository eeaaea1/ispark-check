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
    "AracTipi": "10",
    "YakitTipi": "1"
}

r = requests.post(url, headers=headers, data=data)

print("HTTP:", r.status_code)
print(r.text[:500])
