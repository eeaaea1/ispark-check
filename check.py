
import socket
import requests

host = "ispark.istanbul"

print("1. DNS testi")
try:
    print("IP adresleri:", socket.getaddrinfo(host, 443))
except Exception as e:
    print("DNS HATASI:", repr(e))

print("\n2. HTTPS bağlantı testi")

for url in [
    "https://ispark.istanbul/",
    "https://ispark.istanbul/abone/",
]:
    try:
        r = requests.get(
            url,
            timeout=(8, 10),
            allow_redirects=True
        )
        print("URL:", url)
        print("HTTP:", r.status_code)
        print("Son adres:", r.url)
        print("Yanıt başlangıcı:", repr(r.text[:200]))
    except requests.RequestException as e:
        print("URL:", url)
        print("HATA:", repr(e))
