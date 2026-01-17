import nmap
import requests
import socket
import sys

# SENİN API ADRESİN (Akıllı Kapı - Upsert)
API_URL = "http://localhost:5219/api/assets/register"

def get_local_ip_range():
    """
    Bilgisayarın kendi IP adresini bulur ve ağ aralığını tahmin eder.
    Örn: IP 192.168.1.45 ise Ağ: 192.168.1.0/24 döndürür.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Google DNS'e bağlanıyormuş gibi yapıp yerel IP'yi öğrenir (Bağlantı kurmaz)
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
        ip_parts = IP.split('.')
        # Son kısmı 0 yapıp /24 ekle
        return f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    except Exception as e:
        print(f"⚠️ IP Aralığı bulunamadı, varsayılan kullanılıyor: 192.168.1.0/24")
        return "192.168.1.0/24" 
    finally:
        s.close()

def agi_tara():
    # Nmap Nesnesi Oluştur
    nm = nmap.PortScanner()
    
    # Hedef Ağı Belirle
    hedef_ag = get_local_ip_range()
    
    print(f"\n📡 RADAR AKTİF: {hedef_ag} ağı taranıyor...")
    print("⏳ Lütfen bekleyin, bu işlem ağ büyüklüğüne göre 10-30 saniye sürebilir...\n")
    
    try:
        # TARAMA BAŞLAT
        # -sn: Ping Scan (Port taraması yapma, sadece kim ayakta ona bak)
        # sudo ile çalıştırılırsa MAC adreslerini de bulur.
        nm.scan(hosts=hedef_ag, arguments='-sn')
    except nmap.PortScannerError:
        print("❌ HATA: Nmap bulunamadı! 'sudo dnf install nmap' yaptınız mı?")
        return
    except Exception as e:
        print(f"❌ HATA: {e}")
        return

    bulunanlar = nm.all_hosts()
    print(f"✅ TARAMA BİTTİ! Toplam {len(bulunanlar)} cihaz tespit edildi.\n")

    for ip in bulunanlar:
        try:
            cihaz_bilgisi = nm[ip]
            
            # 1. Cihaz Adı (Hostname)
            hostname = cihaz_bilgisi.hostname()
            if not hostname:
                hostname = f"Unknown_Device_{ip}"
            
            # 2. MAC Adresi (KRİTİK!)
            # MAC adresi yoksa Nmap root yetkisiyle çalışmıyor demektir.
            mac_address = ""
            vendor = ""
            
            if 'addresses' in cihaz_bilgisi and 'mac' in cihaz_bilgisi['addresses']:
                mac_address = cihaz_bilgisi['addresses']['mac']
                
                # Üretici Bilgisi (Örn: Apple, Samsung, TP-Link)
                if 'vendor' in cihaz_bilgisi and mac_address in cihaz_bilgisi['vendor']:
                    vendor = cihaz_bilgisi['vendor'][mac_address]
            else:
                print(f"⚠️  ATLANDI: {ip} (MAC Adresi okunamadı - sudo gerekli)")
                continue # MAC yoksa kaydetme, çünkü kimliksiz cihaz olmaz.

            print(f"➡️  BULUNDU: {hostname} | {ip} | {mac_address} | {vendor}")

            # 3. Veriyi Hazırla
            veri = {
                "name": f"{hostname} ({vendor})", # Adı üreticiyle beraber yazalım
                "macAddress": mac_address,
                "ipAddress": ip, # Modelde 'Ipaddress' ise backend map eder.
                "assetTypeId": 2, # 2: Diğer (PC değil)
                "status": "Active",
                "osVersion": "Nmap Scan", 
                "description": f"Otomatik Ağ Taraması: {vendor}"
            }

            # 4. API'ye Gönder
            resp = requests.post(API_URL, json=veri)
            
            if resp.status_code in [200, 201]:
                print(f"   💾 Veritabanına İşlendi.")
            else:
                print(f"   ❌ API Hatası: {resp.status_code}")

        except Exception as e:
            print(f"   ⚠️  Hata ({ip}): {e}")

if __name__ == "__main__":
    # Kullanıcıyı uyar: Sudo lazım!
    import os
    if os.geteuid() != 0:
        print("\n🛑 DİKKAT: MAC adreslerini okuyabilmek için bu scripti 'SUDO' ile çalıştırmalısınız!")
        print("👉 Kullanım: sudo env \"PATH=$PATH\" python network_scanner.py\n")
    else:
        agi_tara()