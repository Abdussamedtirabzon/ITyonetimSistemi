import requests
import json

# Bizim C# API'nin adresi
API_URL = "http://localhost:5219/api/assets"

def verileri_getir():
    print(f"📡 API'ye bağlanılıyor: {API_URL}...")
    
    try:
        # API'ye istek at (GET)
        cevap = requests.get(API_URL)
        
        # Eğer cevap kodu 200 (Başarılı) ise
        if cevap.status_code == 200:
            varliklar = cevap.json()
            print(f"✅ Bağlantı Başarılı! Toplam {len(varliklar)} cihaz bulundu.\n")
            
            # Gelen verileri tek tek yazdır
            for cihaz in varliklar:
                print(f"🖥️  {cihaz['name']} ({cihaz['assetTypeId']}) - {cihaz['macAddress']}")
                print(f"    Durum: {cihaz['status']}")
                print("-" * 30)
        else:
            print(f"❌ Hata! Sunucu kodu: {cevap.status_code}")
            
    except Exception as e:
        print(f"🔥 Bağlantı Hatası: {e}")
        print("İPUCU: 'dotnet run' ile API'yi çalıştırdın mı?")

if __name__ == "__main__":
    verileri_getir()
