from pathlib import Path

print("Program başladı")

Path("test.txt").write_text("GitHub Actions çalışıyor.", encoding="utf-8")

print("test.txt oluşturuldu")
