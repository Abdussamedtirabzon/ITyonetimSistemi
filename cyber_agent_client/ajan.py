import psutil
import platform
import socket
import requests
import uuid
import json

# API Adresi
API_URL = "http://localhost:5219/api/assets/register"
# --- BİLGİ TOPLAMA FONKSİYONLARI ---

def get_size(bytes, suffix="B"):
    """Byte cinsinden veriyi GB, MB gibi okunabilir formata çevirir"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def sistem_bilgilerini_getir():
    print("🕵️‍♂️ Derinlemesine Tarama Başlatılıyor...")

    # 1. Temel Bilgiler
    cihaz_adi = socket.gethostname()
    mac_adresi = ':'.join((['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1]))
    
    # 2. İşletim Sistemi (OS)
    os_bilgisi = f"{platform.system()} {platform.release()}"
    
    # 3. İşlemci (CPU)
    cpu_bilgisi = platform.processor()
    # Linux bazen processor bilgisini boş döndürür, alternatif:
    if not cpu_bilgisi:
        cpu_bilgisi = platform.machine() 

    # 4. RAM (Bellek)
    ram_byte = psutil.virtual_memory().total
    ram_bilgisi = get_size(ram_byte) # Örn: 15.89 GB

    # 5. Disk (Ana Disk / )
    try:
        disk_byte = psutil.disk_usage('/').total
        disk_bilgisi = get_size(disk_byte) # Örn: 480.00 GB
    except:
        disk_bilgisi = "Bilinmiyor"

    # 6. IP Adresi
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip_adresi = s.getsockname()[0]
    except:
        ip_adresi = '127.0.0.1'
    finally:
        s.close()

    print(f"🖥️  Cihaz: {cihaz_adi}")
    print(f"📀 OS: {os_bilgisi}")
    print(f"🧠 CPU: {cpu_bilgisi}")
    print(f"💾 RAM: {ram_bilgisi} | Disk: {disk_bilgisi}")

    return {
        "name": cihaz_adi,
        "macAddress": mac_adresi,
        "ipAddress": ip_adresi,
        "assetTypeId": 1, 
        "status": "Active",
        "osVersion": os_bilgisi,     # YENİ
        "cpuInfo": cpu_bilgisi,      # YENİ
        "ramCapacity": ram_bilgisi,  # YENİ
        "diskCapacity": disk_bilgisi # YENİ
    }

def veriyi_gonder(veri):
    try:
        # Şimdilik direkt POST (Ekleme) yapıyoruz.
        # İleride: "Bu MAC adresi var mı? Varsa UPDATE et, yoksa POST et" diyeceğiz.
        response = requests.post(API_URL, json=veri)
        
        if response.status_code in [200, 201]:
            print("✅ RAPOR GÖNDERİLDİ: Veriler veritabanına işlendi!")
        else:
            print(f"⚠️ Sunucu Hatası: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Bağlantı Yok: {e}")

if __name__ == "__main__":
    toplanan_veri = sistem_bilgilerini_getir()
    veriyi_gonder(toplanan_veri)