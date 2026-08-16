import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.turksat.com.tr/uydu/yayincilik-hizmetleri/turksat-frekans-listesi"

def fetch_frequencies():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    kanallar = []
    
    # Türksat tablosundaki satırları tara
    for row in soup.select("table tbody tr"):
        cols = [c.get_text(strip=True) for c in row.select("td")]
        if len(cols) >= 8:
            kanallar.append({
                "kanal": cols[0],
                "paket": cols[1],
                "frekans": cols[2],
                "polarizasyon": cols[3],
                "sembol": cols[4],
                "fec": cols[5],
                "kapsama": cols[6],
                "tur": cols[7]
            })
            
    with open("kanallar.json", "w", encoding="utf-8") as f:
        json.dump(kanallar, f, ensure_ascii=False, indent=2)
        
    print(f"Toplam {len(kanallar)} kanal başarıyla kaydedildi.")

if __name__ == "__main__":
    fetch_frequencies()