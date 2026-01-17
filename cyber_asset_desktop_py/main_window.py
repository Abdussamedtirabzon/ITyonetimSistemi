import sys
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QMessageBox, QHeaderView, QLabel,
                             QDialog, QFormLayout, QLineEdit, QComboBox, QTabWidget)
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

# Grafik Kütüphaneleri
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# API Adresleri
# Akıllı kayıt (Mac adresi kontrolü yapan)
API_REGISTER_URL = "http://localhost:5219/api/assets/register"
# Standart işlemler (Listeleme, Silme, Tekli Getirme)
API_BASE_URL = "http://localhost:5219/api/assets"

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
        self.setFixedSize(400, 550) 
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.input_ad = QLineEdit()
        self.combo_tur = QComboBox()
        self.combo_tur.addItems(["Laptop", "Sunucu", "Masaüstü", "Diğer"])
        self.input_seri = QLineEdit() # MAC Adresi
        self.input_seri.setPlaceholderText("Örn: 00:1A:2B:3C:4D:5E")
        self.input_ip = QLineEdit()
        self.combo_durum = QComboBox()
        self.combo_durum.addItems(["Active", "Passive"])

        # Detay Alanları
        self.input_os = QLineEdit()
        self.input_cpu = QLineEdit()
        self.input_ram = QLineEdit()
        self.input_disk = QLineEdit()

        form_layout.addRow("Cihaz Adı:", self.input_ad)
        form_layout.addRow("Türü:", self.combo_tur)
        form_layout.addRow("MAC Adresi:", self.input_seri)
        form_layout.addRow("IP Adresi:", self.input_ip)
        form_layout.addRow("Durum:", self.combo_durum)
        form_layout.addRow("İşletim Sistemi:", self.input_os)
        form_layout.addRow("İşlemci (CPU):", self.input_cpu)
        form_layout.addRow("RAM:", self.input_ram)
        form_layout.addRow("Disk:", self.input_disk)

        layout.addLayout(form_layout)

        self.btn_kaydet = QPushButton("💾 Kaydet")
        self.btn_kaydet.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold;")
        self.btn_kaydet.clicked.connect(self.kaydet)
        layout.addWidget(self.btn_kaydet)
        self.setLayout(layout)

    def kaydet(self):
        ad = self.input_ad.text()
        mac = self.input_seri.text()
        if not ad or not mac:
            QMessageBox.warning(self, "Eksik", "Cihaz adı ve MAC adresi zorunludur!")
            return

        tur_secim = self.combo_tur.currentText()
        asset_type_id = 1 if tur_secim == "Laptop" else 2

        yeni_veri = {
            "name": ad, 
            "macAddress": mac, 
            "ipAddress": self.input_ip.text(),
            "assetTypeId": asset_type_id,
            "status": self.combo_durum.currentText(),
            "osVersion": self.input_os.text(),
            "cpuInfo": self.input_cpu.text(),
            "ramCapacity": self.input_ram.text(),
            "diskCapacity": self.input_disk.text()
        }

        try:
            # Akıllı kayıt kapısına gönderiyoruz (Varsa günceller, yoksa ekler)
            requests.post(API_REGISTER_URL, json=yeni_veri)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bağlantı: {e}")

# --- 2. DÜZENLEME PENCERESİ ---
class DuzenleDialog(QDialog):
    def __init__(self, asset_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Düzenle: {asset_data.get('name')}")
        self.setFixedSize(400, 550)
        self.asset_data = asset_data
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.input_ad = QLineEdit(asset_data.get('name'))
        
        self.combo_tur = QComboBox()
        self.combo_tur.addItems(["Laptop", "Sunucu", "Masaüstü", "Diğer"])
        if asset_data.get('assetTypeId') == 1: self.combo_tur.setCurrentText("Laptop")
        else: self.combo_tur.setCurrentText("Diğer")
        
        self.input_seri = QLineEdit(asset_data.get('macAddress'))
        self.input_ip = QLineEdit(asset_data.get('ipAddress') or "")

        self.combo_durum = QComboBox()
        self.combo_durum.addItems(["Active", "Passive"])
        self.combo_durum.setCurrentText(asset_data.get('status'))

        # Detaylar
        self.input_os = QLineEdit(asset_data.get('osVersion') or "")
        self.input_cpu = QLineEdit(asset_data.get('cpuInfo') or "")
        self.input_ram = QLineEdit(asset_data.get('ramCapacity') or "")
        self.input_disk = QLineEdit(asset_data.get('diskCapacity') or "")

        form_layout.addRow("Cihaz Adı:", self.input_ad)
        form_layout.addRow("Türü:", self.combo_tur)
        form_layout.addRow("MAC Adresi:", self.input_seri)
        form_layout.addRow("IP Adresi:", self.input_ip)
        form_layout.addRow("Durum:", self.combo_durum)
        form_layout.addRow("İşletim Sistemi:", self.input_os)
        form_layout.addRow("İşlemci:", self.input_cpu)
        form_layout.addRow("RAM:", self.input_ram)
        form_layout.addRow("Disk:", self.input_disk)

        layout.addLayout(form_layout)

        self.btn_guncelle = QPushButton("✏️ Güncelle")
        self.btn_guncelle.setStyleSheet("background-color: #e67e22; color: white; padding: 10px; font-weight: bold;")
        self.btn_guncelle.clicked.connect(self.guncelle)
        layout.addWidget(self.btn_guncelle)

        self.setLayout(layout)

    def guncelle(self):
        tur_secim = self.combo_tur.currentText()
        asset_type_id = 1 if tur_secim == "Laptop" else 2
        
        guncel_veri = {
            "id": self.asset_data.get('id'),
            "name": self.input_ad.text(),
            "macAddress": self.input_seri.text(),
            "ipAddress": self.input_ip.text(),
            "assetTypeId": asset_type_id,
            "status": self.combo_durum.currentText(),
            # Yeni alanlar
            "osVersion": self.input_os.text(),
            "cpuInfo": self.input_cpu.text(),
            "ramCapacity": self.input_ram.text(),
            "diskCapacity": self.input_disk.text()
        }

        try:
            url = f"{API_BASE_URL}/{self.asset_data.get('id')}"
            requests.put(url, json=guncel_veri)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Hata: {e}")

# --- 3. GRAFİK ALANI ---
class GrafikCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # Koyu Tema İçin Arka Plan
        self.fig.patch.set_facecolor('#353535') 
        super().__init__(self.fig)

# --- 4. ANA PENCERE ---
class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOC Dashboard - IT Varlık Yönetimi")
        self.setGeometry(100, 100, 1200, 700)

        # Sekme Yapısı
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 1. SEKME: Cihaz Listesi
        self.tab_liste = QWidget()
        self.setup_liste_tab()
        self.tabs.addTab(self.tab_liste, "📋 Cihaz Envanteri")

        # 2. SEKME: Analiz Grafikleri
        self.tab_grafik = QWidget()
        self.setup_grafik_tab()
        self.tabs.addTab(self.tab_grafik, "📊 Analiz & Dashboard")

        self.verileri_yukle()

    def setup_liste_tab(self):
        layout = QVBoxLayout()
        
        # Üst Butonlar (Ekle / Düzenle / Yenile / Sil)
        ust_kisim = QHBoxLayout()
        
        self.btn_ekle = QPushButton("➕ Yeni Ekle")
        self.btn_ekle.setStyleSheet("background-color: #27ae60; color: white; padding: 8px; border: none;")
        self.btn_ekle.clicked.connect(self.pencere_ac_ekle)
        ust_kisim.addWidget(self.btn_ekle)

        self.btn_duzenle = QPushButton("✏️ Düzenle")
        self.btn_duzenle.setStyleSheet("background-color: #f39c12; color: white; padding: 8px; border: none;")
        self.btn_duzenle.clicked.connect(self.pencere_ac_duzenle)
        ust_kisim.addWidget(self.btn_duzenle)

        self.btn_yenile = QPushButton("🔄 Yenile")
        self.btn_yenile.setStyleSheet("background-color: #2980b9; color: white; padding: 8px; border: none;")
        self.btn_yenile.clicked.connect(self.verileri_yukle)
        ust_kisim.addWidget(self.btn_yenile)

        # Boşluk Bırak
        ust_kisim.addStretch()

        self.btn_sil = QPushButton("🗑️ Seçiliyi Sil")
        self.btn_sil.setStyleSheet("background-color: #c0392b; color: white; padding: 8px; border: none;")
        self.btn_sil.clicked.connect(self.varlik_sil)
        ust_kisim.addWidget(self.btn_sil)

        layout.addLayout(ust_kisim)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(9)
        self.tablo.setHorizontalHeaderLabels(["ID", "Ad", "Tür", "MAC", "IP", "Durum", "OS", "RAM", "Son Görülme"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tablo.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tablo.setStyleSheet("alternate-background-color: #444; background-color: #333; color: white;")
        layout.addWidget(self.tablo)

        self.tab_liste.setLayout(layout)

    def setup_grafik_tab(self):
        layout = QVBoxLayout()
        
        lbl_info = QLabel("İşletim Sistemi Dağılımı")
        lbl_info.setStyleSheet("font-size: 16px; font-weight: bold; color: white; margin: 10px;")
        lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_info)

        self.grafik = GrafikCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.grafik)

        self.tab_grafik.setLayout(layout)

    def verileri_yukle(self):
        try:
            response = requests.get(API_BASE_URL)
            if response.status_code == 200:
                data = response.json()
                self.tablo_doldur(data)
                self.grafik_ciz(data)
        except Exception as e:
            print(f"Hata: {e}")

    def tablo_doldur(self, veriler):
        self.tablo.setRowCount(len(veriler))
        for i, veri in enumerate(veriler):
            self.hucre_yaz(i, 0, veri.get('id'))
            self.hucre_yaz(i, 1, veri.get('name'))
            self.hucre_yaz(i, 2, "PC" if veri.get('assetTypeId')==1 else "Diğer")
            self.hucre_yaz(i, 3, veri.get('macAddress'))
            self.hucre_yaz(i, 4, veri.get('ipAddress'))
            self.hucre_yaz(i, 5, veri.get('status'))
            self.hucre_yaz(i, 6, veri.get('osVersion'))
            self.hucre_yaz(i, 7, veri.get('ramCapacity'))
            self.hucre_yaz(i, 8, veri.get('lastSeen'))

            # Pasif cihazları kırmızı yap
            if veri.get('status') != "Active":
                for col in range(9):
                    self.tablo.item(i, col).setBackground(QColor("#7f0000"))

    def hucre_yaz(self, row, col, val):
        if val is None: val = "-"
        item = QTableWidgetItem(str(val))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tablo.setItem(row, col, item)

    def grafik_ciz(self, veriler):
        # İşletim Sistemlerini Say
        os_counts = {}
        for veri in veriler:
            os_name = veri.get('osVersion')
            if not os_name: 
                os_name = "Bilinmiyor"
            else:
                os_name = os_name.split()[0] # Fedora Linux 39 -> Fedora
            
            os_counts[os_name] = os_counts.get(os_name, 0) + 1

        labels = list(os_counts.keys())
        sizes = list(os_counts.values())
        
        # Grafiği Temizle ve Çiz
        self.grafik.axes.clear()
        wedges, texts, autotexts = self.grafik.axes.pie(
            sizes, labels=labels, autopct='%1.1f%%', 
            startangle=90, colors=['#3498db', '#e74c3c', '#2ecc71', '#f1c40f']
        )
        
        # Yazı Renklerini Ayarla (Koyu Tema İçin)
        for text in texts: text.set_color('white')
        for autotext in autotexts: autotext.set_color('white')
        
        self.grafik.draw()

    def pencere_ac_ekle(self):
        dialog = EkleDialog(self)
        if dialog.exec(): self.verileri_yukle()

    def pencere_ac_duzenle(self):
        secili = self.tablo.selectionModel().selectedRows()
        if not secili:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir cihaz seçin!")
            return
        
        rid = secili[0].row()
        secili_id = self.tablo.item(rid, 0).text()
        
        try:
            resp = requests.get(f"{API_BASE_URL}/{secili_id}")
            if resp.status_code == 200:
                dialog = DuzenleDialog(resp.json(), self)
                if dialog.exec(): self.verileri_yukle()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def varlik_sil(self):
        secili = self.tablo.selectionModel().selectedRows()
        if not secili: 
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir cihaz seçin!")
            return
        
        rid = secili[0].row()
        id_val = self.tablo.item(rid, 0).text()
        
        cevap = QMessageBox.question(self, "Onay", "Bu cihazı silmek istiyor musunuz?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if cevap == QMessageBox.StandardButton.Yes:
            requests.delete(f"{API_BASE_URL}/{id_val}")
            self.verileri_yukle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # DARK THEME RENKLERİ
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    p.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    p.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    p.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    p.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    p.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    p.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    p.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    p.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    p.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(p)

    giris = GirisPenceresi()
    if giris.exec():
        win = AnaPencere()
        win.show()
        sys.exit(app.exec())
    else:
        sys.exit()