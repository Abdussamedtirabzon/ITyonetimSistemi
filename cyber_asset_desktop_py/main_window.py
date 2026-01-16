import sys
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QMessageBox, QHeaderView, QLabel)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

# API Adresi
API_URL = "http://localhost:5219/api/assets"

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IT Varlık Yönetimi - Linux Admin Paneli")
        self.setGeometry(100, 100, 900, 600)

        # --- Arayüz Düzeni ---
        ana_layout = QVBoxLayout()
        buton_layout = QHBoxLayout() # Butonları yan yana koymak için

        # Başlık
        baslik = QLabel("🚀 Siber Varlık Kontrol Merkezi")
        baslik.setStyleSheet("font-size: 18px; font-weight: bold; color: #44bd32;")
        ana_layout.addWidget(baslik)

        # 1. Yenile Butonu
        self.btn_yenile = QPushButton("🔄 Listeyi Yenile")
        self.btn_yenile.setStyleSheet("background-color: #3498db; color: white; padding: 8px; font-weight: bold;")
        self.btn_yenile.clicked.connect(self.verileri_yukle)
        buton_layout.addWidget(self.btn_yenile)

        # 2. Sil Butonu (YENİ EKLENDİ)
        self.btn_sil = QPushButton("🗑️ Seçili Olanı Sil")
        self.btn_sil.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; font-weight: bold;")
        self.btn_sil.clicked.connect(self.varlik_sil) # Tıklayınca silme fonksiyonuna git
        buton_layout.addWidget(self.btn_sil)

        ana_layout.addLayout(buton_layout)

        # 3. Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(["ID", "Cihaz Adı", "Tür", "Seri No / MAC", "Durum"])
        
        # Tablo ayarları
        header = self.tablo.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Tek tıkla tüm satırı seç
        self.tablo.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Sadece tek satır seçilebilsin
        
        ana_layout.addWidget(self.tablo)

        # Ana Widget'ı ayarla
        container = QWidget()
        container.setLayout(ana_layout)
        self.setCentralWidget(container)

        # Başlangıçta verileri çek
        self.verileri_yukle()

    def verileri_yukle(self):
        """API'den verileri çeker ve tabloya yazar"""
        print("Veriler yükleniyor...")
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                self.tablo_doldur(response.json())
            else:
                QMessageBox.warning(self, "Hata", f"API Hatası: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", f"Sunucuya ulaşılamadı!\n\n{str(e)}")

    def tablo_doldur(self, veri_listesi):
        self.tablo.setRowCount(0) # Tabloyu temizle
        self.tablo.setRowCount(len(veri_listesi)) 

        for satir_no, veri in enumerate(veri_listesi):
            # ID (Gizli kahraman, silerken lazım olacak)
            self.hucre_ekle(satir_no, 0, str(veri.get('id')))
            self.hucre_ekle(satir_no, 1, veri.get('name'))
            
            tur = "Laptop" if veri.get('assetTypeId') == 1 else "Diğer"
            self.hucre_ekle(satir_no, 2, tur)
            
            self.hucre_ekle(satir_no, 3, veri.get('macAddress'))
            
            durum = veri.get('status', 'Passive')
            self.hucre_ekle(satir_no, 4, durum)

            # Pasifleri Kırmızı Yap
            if durum != "Active":
                for i in range(5):
                    self.tablo.item(satir_no, i).setBackground(QColor("#ffcccc"))

    def hucre_ekle(self, satir, sutun, yazi):
        item = QTableWidgetItem(str(yazi))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tablo.setItem(satir, sutun, item)

    # --- YENİ EKLENEN SİLME FONKSİYONU ---
    def varlik_sil(self):
        # 1. Seçili satır var mı?
        secili_satirlar = self.tablo.selectionModel().selectedRows()
        if not secili_satirlar:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir cihaz seçin!")
            return

        # 2. Seçili satırın ID'sini al (0. sütunda ID var)
        secili_index = secili_satirlar[0].row()
        cihaz_id = self.tablo.item(secili_index, 0).text()
        cihaz_adi = self.tablo.item(secili_index, 1).text()

        # 3. Son Karar? (Emin misin?)
        cevap = QMessageBox.question(
            self, "Silme Onayı", 
            f"⚠️ '{cihaz_adi}' cihazını kalıcı olarak silmek istiyor musun?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if cevap == QMessageBox.StandardButton.Yes:
            try:
                # 4. API'ye SİL emrini gönder (DELETE Request)
                full_url = f"{API_URL}/{cihaz_id}"
                response = requests.delete(full_url)

                if response.status_code in [200, 204]:
                    QMessageBox.information(self, "Başarılı", "Cihaz silindi! 🗑️")
                    self.verileri_yukle() # Listeyi yenile
                else:
                    QMessageBox.warning(self, "Hata", f"Silinemedi! Kod: {response.status_code}")

            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bir sorun oluştu: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec())