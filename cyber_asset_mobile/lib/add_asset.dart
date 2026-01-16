import 'package:flutter/material.dart';

class AddAssetPage extends StatefulWidget {
  const AddAssetPage({super.key});

  @override
  State<AddAssetPage> createState() => _AddAssetPageState();
}

class _AddAssetPageState extends State<AddAssetPage> {
  // Formdaki verileri tutacak değişkenler
  final _adController = TextEditingController();
  final _seriNoController = TextEditingController();
  String _secilenTur = 'Laptop'; // Varsayılan değer

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Yeni Varlık Ekle"),
        backgroundColor: Colors.transparent,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("Cihaz Bilgileri", style: TextStyle(color: Colors.cyanAccent, fontSize: 18)),
            const SizedBox(height: 20),

            // 1. Cihaz Adı
            _buildTextField(label: "Cihaz Adı / Model", icon: Icons.computer, controller: _adController),
            const SizedBox(height: 15),

            // 2. Seri Numarası
            _buildTextField(label: "Seri Numarası", icon: Icons.qr_code, controller: _seriNoController),
            const SizedBox(height: 15),

            // 3. Cihaz Türü (Açılır Menü)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
              decoration: BoxDecoration(
                color: Colors.white10,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey.shade700),
              ),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
                  value: _secilenTur,
                  dropdownColor: const Color(0xFF2C2C2C),
                  isExpanded: true,
                  icon: const Icon(Icons.arrow_drop_down, color: Colors.cyanAccent),
                  items: ['Laptop', 'Monitör', 'Telefon', 'Tablet', 'Yazıcı', 'Ağ Cihazı']
                      .map((String value) {
                    return DropdownMenuItem<String>(
                      value: value,
                      child: Text(value, style: const TextStyle(color: Colors.white)),
                    );
                  }).toList(),
                  onChanged: (newValue) {
                    setState(() {
                      _secilenTur = newValue!;
                    });
                  },
                ),
              ),
            ),
            const SizedBox(height: 40),

            // KAYDET BUTONU
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton.icon(
                // add_asset.dart içinde KAYDET butonu kısmı:
onPressed: () {
  if (_adController.text.isEmpty || _seriNoController.text.isEmpty) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Lütfen tüm alanları doldurun!")),
    );
    return;
  }

  // 1. Yeni veriyi bir paket (Map) yap
  final yeniCihaz = {
    "isim": _adController.text,
    "tur": _secilenTur,
    "durum": true, // Varsayılan olarak sağlam (Aktif) olsun
  };

  // 2. Bu paketi önceki sayfaya fırlat ve penceryi kapat
  Navigator.pop(context, yeniCihaz);
},
                icon: const Icon(Icons.save),
                label: const Text("KAYDET"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.cyanAccent,
                  foregroundColor: Colors.black,
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  // Özel Text Kutusu Tasarımı (Kod tekrarını önlemek için)
  Widget _buildTextField({required String label, required IconData icon, required TextEditingController controller}) {
    return TextField(
      controller: controller,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        prefixIcon: Icon(icon, color: Colors.grey),
        filled: true,
        fillColor: Colors.white10,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.grey.shade800),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Colors.cyanAccent),
        ),
      ),
    );
  }
}