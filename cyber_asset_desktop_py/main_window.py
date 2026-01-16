import sys
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QMessageBox, QHeaderView, QLabel,
                             QDialog, QFormLayout, QLineEdit, QComboBox)
from PyQt6.QtGui import QColor, QPalette, QIcon
from PyQt6.QtCore import Qt

# API Adresi
API_URL = "http://localhost:5219/api/assets"

# --- 0. GİRİŞ EKRANI (LOGIN) ---
class GirisPenceresi(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Güvenli Giriş")
        self.setFixedSize(350, 250)
        
        layout = QVBoxLayout()

        lbl_baslik = QLabel("🔐 SİBER GİRİŞ")
        lbl_baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_baslik.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #ecf0f1;")
        layout.addWidget(lbl_baslik)

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Kullanıcı Adı")
        self.txt_user.setStyleSheet("padding: 8px; border-radius: 4px;")
        layout.addWidget(self.txt_user)

        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Şifre")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass.setStyleSheet("padding: 8px; border-radius: 4px;")
        layout.addWidget(self.txt_pass)

        self.btn_giris = QPushButton("GİRİŞ YAP")
        self.btn_giris.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_giris.setStyleSheet("background-color: #e67e22; color: white; padding: 10px; font-weight: bold; border-radius: 5px; margin-top: 10px;")
        self.btn_giris.clicked.connect(self.kontrol_et)
        layout.addWidget(self.btn_giris)

        self.setLayout(layout)

    def kontrol_et(self):
        if self.txt_user.text() == "admin" and self.txt_pass.text() == "1234":
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "⛔ Yanlış Kullanıcı Adı veya Şifre!")

# --- 1. EKLEME PENCERESİ ---
class EkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Cihaz Ekle")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.input_ad = QLineEdit()
        self.combo_tur = QComboBox()
        self.combo_tur.addItems(["Laptop", "Sunucu", "Masaüstü", "Diğer"])
        self.input_seri = QLineEdit()
        self.input_seri.setPlaceholderText("Örn: AA:BB:CC:11:22:33")
        self.combo_durum = QComboBox()
        self.combo_durum.addItems(["Active", "Passive"])

        form_layout.addRow("Cihaz Adı:", self.input_ad)
        form_layout.addRow("Türü:", self.combo_tur)
        form_layout.addRow("Seri No / MAC:", self.input_seri)
        form_layout.addRow("Durum:", self.combo_durum)

        layout.addLayout(form_layout)

        self.btn_kaydet = QPushButton("💾 Kaydet")
        self.btn_kaydet.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold;")
        self.btn_kaydet.clicked.connect(self.kaydet)
        layout.addWidget(self.btn_kaydet)
        self.setLayout(layout)

    def kaydet(self):
        ad = self.input_ad.text()
        seri = self.input_seri.text()
        if not ad or not seri:
            QMessageBox.warning(self, "Eksik", "Lütfen İsim ve Seri No doldurun!")
            return

        tur_secim = self.combo_tur.currentText()
        asset_type_id = 1 if tur_secim == "Laptop" else 2

        yeni_veri = {
            "name": ad, "macAddress": seri, "assetTypeId": asset_type_id,
            "status": self.combo_durum.currentText(), "ipAddress": "192.168.1.100"
        }

        try:
            requests.post(API_URL, json=yeni_veri)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bağlantı: {e}")

# --- 2. DÜZENLEME PENCERESİ (YENİ) ---
class DuzenleDialog(QDialog):
    def __init__(self, asset_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Düzenle: {asset_data.get('name')}")
        self.setFixedSize(400, 300)
        self.asset_data = asset_data # Eski veriyi sakla
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Alanlar (Eski verilerle dolu gelecek)
        self.input_ad = QLineEdit(asset_data.get('name'))
        
        self.combo_tur = QComboBox()
        self.combo_tur.addItems(["Laptop", "Sunucu", "Masaüstü", "Diğer"])
        # Türü seçili getir (Basit mantık)
        eski_tur_id = asset_data.get('assetTypeId')
        if eski_tur_id == 1: self.combo_tur.setCurrentText("Laptop")
        else: self.combo_tur.setCurrentText("Diğer")
        
        self.input_seri = QLineEdit(asset_data.get('macAddress'))

        self.combo_durum = QComboBox()
        self.combo_durum.addItems(["Active", "Passive"])
        self.combo_durum.setCurrentText(asset_data.get('status'))

        form_layout.addRow("Cihaz Adı:", self.input_ad)
        form_layout.addRow("Türü:", self.combo_tur)
        form_layout.addRow("Seri No / MAC:", self.input_seri)
        form_layout.addRow("Durum:", self.combo_durum)

        layout.addLayout(form_layout)

        # Güncelle Butonu
        self.btn_guncelle = QPushButton("✏️ Güncelle")
        self.btn_guncelle.setStyleSheet("background-color: #e67e22; color: white; padding: 10px; font-weight: bold;")
        self.btn_guncelle.clicked.connect(self.guncelle)
        layout.addWidget(self.btn_guncelle)

        self.setLayout(layout)

    def guncelle(self):
        # Yeni verileri hazırla
        tur_secim = self.combo_tur.currentText()
        asset_type_id = 1 if tur_secim == "Laptop" else 2
        
        guncel_veri = {
            "id": self.asset_data.get('id'), # ID değişmez
            "name": self.input_ad.text(),
            "macAddress": self.input_seri.text(),
            "assetTypeId": asset_type_id,
            "status": self.combo_durum.currentText(),
            "ipAddress": self.asset_data.get('ipAddress', '192.168.1.100') # Eski IP'yi koru
        }

        # API'ye PUT isteği at
        try:
            url = f"{API_URL}/{self.asset_data.get('id')}"
            response = requests.put(url, json=guncel_veri)
            
            if response.status_code in [200, 204]:
                QMessageBox.information(self, "Başarılı", "Güncelleme tamamlandı! ✅")
                self.accept()
            else:
                QMessageBox.warning(self, "Hata", f"Güncellenemedi! Kod: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bağlantı hatası: {e}")


# --- 3. ANA PENCERE ---
class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IT Varlık Yönetimi - Linux Admin Paneli")
        self.setGeometry(100, 100, 950, 600)

        ana_widget = QWidget()
        ana_layout = QVBoxLayout()
        
        # Üst Panel
        ust_kisim = QHBoxLayout()
        baslik = QLabel("🚀 Siber Varlık Kontrol Merkezi")
        baslik.setStyleSheet("font-size: 18px; font-weight: bold; color: #9b59b6;") 
        ust_kisim.addWidget(baslik)
        ust_kisim.addStretch()

        # --- BUTONLAR ---
        self.btn_ekle = QPushButton("➕ Yeni Ekle")
        self.btn_ekle.setStyleSheet("background-color: #27ae60; color: white; padding: 8px; border: none;")
        self.btn_ekle.clicked.connect(self.pencere_ac_ekle)
        ust_kisim.addWidget(self.btn_ekle)

        # YENİ EKLENEN BUTON
        self.btn_duzenle = QPushButton("✏️ Düzenle")
        self.btn_duzenle.setStyleSheet("background-color: #f39c12; color: white; padding: 8px; border: none;")
        self.btn_duzenle.clicked.connect(self.pencere_ac_duzenle)
        ust_kisim.addWidget(self.btn_duzenle)

        self.btn_yenile = QPushButton("🔄 Yenile")
        self.btn_yenile.setStyleSheet("background-color: #2980b9; color: white; padding: 8px; border: none;")
        self.btn_yenile.clicked.connect(self.verileri_yukle)
        ust_kisim.addWidget(self.btn_yenile)

        self.btn_sil = QPushButton("🗑️ Sil")
        self.btn_sil.setStyleSheet("background-color: #c0392b; color: white; padding: 8px; border: none;")
        self.btn_sil.clicked.connect(self.varlik_sil)
        ust_kisim.addWidget(self.btn_sil)

        ana_layout.addLayout(ust_kisim)

        # TABLO
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(["ID", "Cihaz Adı", "Tür", "Seri No", "Durum"])
        
        self.tablo.setStyleSheet("""
            QHeaderView::section { background-color: #353535; color: white; padding: 4px; border: 1px solid #555; }
            QTableWidget { gridline-color: #555; color: #ddd; }
            QTableWidget::item:selected { background-color: #d35400; color: white; }
        """)

        header = self.tablo.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        ana_layout.addWidget(self.tablo)

        ana_widget.setLayout(ana_layout)
        self.setCentralWidget(ana_widget)
        self.verileri_yukle()

    def verileri_yukle(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                self.tablo_doldur(response.json())
        except: pass

    def tablo_doldur(self, veriler):
        self.tablo.setRowCount(len(veriler))
        for i, veri in enumerate(veriler):
            self.hucre_yaz(i, 0, veri.get('id'))
            self.hucre_yaz(i, 1, veri.get('name'))
            self.hucre_yaz(i, 2, "Laptop" if veri.get('assetTypeId')==1 else "Diğer")
            self.hucre_yaz(i, 3, veri.get('macAddress'))
            durum = veri.get('status')
            self.hucre_yaz(i, 4, durum)
            
            if durum != "Active":
                for col in range(5):
                    self.tablo.item(i, col).setBackground(QColor("#7f0000"))

    def hucre_yaz(self, row, col, val):
        item = QTableWidgetItem(str(val))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tablo.setItem(row, col, item)

    def pencere_ac_ekle(self):
        dialog = EkleDialog(self)
        if dialog.exec(): self.verileri_yukle()

    # --- DÜZENLEME MANTIĞI ---
    def pencere_ac_duzenle(self):
        secili = self.tablo.selectionModel().selectedRows()
        if not secili:
            QMessageBox.warning(self, "Uyarı", "Düzenlemek için bir cihaz seçin!")
            return

        # 1. Seçili ID'yi al
        rid = secili[0].row()
        secili_id = self.tablo.item(rid, 0).text()

        # 2. Güncel veriyi API'den çek (En doğrusu budur)
        try:
            resp = requests.get(f"{API_URL}/{secili_id}")
            if resp.status_code == 200:
                asset_data = resp.json()
                # 3. Düzenleme penceresini aç
                dialog = DuzenleDialog(asset_data, self)
                if dialog.exec(): 
                    self.verileri_yukle() # Listeyi yenile
            else:
                QMessageBox.warning(self, "Hata", "Veri çekilemedi!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bağlantı: {e}")

    def varlik_sil(self):
        secili = self.tablo.selectionModel().selectedRows()
        if not secili:
            QMessageBox.warning(self, "Uyarı", "Silinecek satırı seçin!")
            return
        
        rid = secili[0].row()
        id_val = self.tablo.item(rid, 0).text()
        
        soru = QMessageBox.question(self, "Onay", "Bu cihaz kalıcı olarak silinsin mi?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if soru == QMessageBox.StandardButton.Yes:
            requests.delete(f"{API_URL}/{id_val}")
            self.verileri_yukle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # DARK MODE PALETİ
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(dark_palette)

    giris = GirisPenceresi()
    if giris.exec():
        win = AnaPencere()
        win.show()
        sys.exit(app.exec())
    else:
        sys.exit()