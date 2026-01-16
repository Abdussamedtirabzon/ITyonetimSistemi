import 'package:flutter/material.dart';
import 'models/asset_model.dart';

class AddAssetPage extends StatefulWidget {
  // Eğer bu sayfaya bir Cihaz (Asset) gönderilirse "Düzenleme Modu" açılır.
  // Gönderilmezse "Ekleme Modu" çalışır.
  final Asset? assetToEdit;

  const AddAssetPage({super.key, this.assetToEdit});

  @override
  State<AddAssetPage> createState() => _AddAssetPageState();
}

class _AddAssetPageState extends State<AddAssetPage> {
  final _adController = TextEditingController();
  final _seriNoController = TextEditingController();
  String _secilenTur = 'Laptop';
  bool _isEditing = false; // Düzenleme modunda mıyız?

  @override
  void initState() {
    super.initState();
    // Eğer düzenlenecek veri geldiyse, kutuları doldur
    if (widget.assetToEdit != null) {
      _isEditing = true;
      _adController.text = widget.assetToEdit!.isim;
      _seriNoController.text = widget.assetToEdit!.seriNo;
      
      // Gelen tür listede var mı kontrol et (Yoksa varsayılan kalsın)
      List<String> turler = ['Laptop', 'Monitör', 'Telefon', 'Tablet', 'Yazıcı', 'Ağ Cihazı', 'Diğer'];
      if (turler.contains(widget.assetToEdit!.tur)) {
        _secilenTur = widget.assetToEdit!.tur;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_isEditing ? "Varlığı Düzenle" : "Yeni Varlık Ekle"),
        backgroundColor: Colors.transparent,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            _buildTextField(label: "Cihaz Adı", icon: Icons.computer, controller: _adController),
            const SizedBox(height: 15),
            _buildTextField(label: "Seri No / MAC", icon: Icons.qr_code, controller: _seriNoController),
            const SizedBox(height: 15),
            
            // Tür Seçimi
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12),
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
                  items: ['Laptop', 'Monitör', 'Telefon', 'Tablet', 'Yazıcı', 'Ağ Cihazı', 'Diğer']
                      .map((e) => DropdownMenuItem(value: e, child: Text(e, style: const TextStyle(color: Colors.white))))
                      .toList(),
                  onChanged: (v) => setState(() => _secilenTur = v!),
                ),
              ),
            ),
            const SizedBox(height: 40),

            // KAYDET BUTONU
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton.icon(
                onPressed: () {
                  if (_adController.text.isEmpty) return;

                  // Verileri paketle
                  final assetData = {
                    "id": widget.assetToEdit?.id, // ID varsa koy (Update için lazım)
                    "isim": _adController.text,
                    "tur": _secilenTur,
                    "seriNo": _seriNoController.text,
                    "durum": true,
                  };

                  // Paketi geri gönder
                  Navigator.pop(context, assetData);
                },
                icon: Icon(_isEditing ? Icons.update : Icons.save),
                label: Text(_isEditing ? "GÜNCELLE" : "KAYDET"),
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
      ),
    );
  }
}