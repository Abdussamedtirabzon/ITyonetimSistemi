import 'package:flutter/material.dart';
import 'add_asset.dart';
import 'services/api_service.dart'; // Servisimizi çağırdık
import 'models/asset_model.dart';   // Modelimizi çağırdık

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final ApiService _apiService = ApiService(); // Postacımızı hazırladık
  late Future<List<Asset>> _assetsFuture; // Gelecek olan verileri tutacak kutu

  @override
  void initState() {
    super.initState();
    _refreshList(); // Sayfa açılınca verileri çek
  }

  // Listeyi Yenileme Fonksiyonu
  void _refreshList() {
    setState(() {
      _assetsFuture = _apiService.getAssets();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('IT Varlık Yönetimi'),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshList, // Manuel yenileme butonu
          ),
        ],
      ),
      drawer: _buildDrawer(context), // Yan menüyü aşağıda tanımladık
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("Envanter Listesi", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),

            // CANLI LİSTE (API'den gelen veriler)
            Expanded(
              child: FutureBuilder<List<Asset>>(
                future: _assetsFuture,
                builder: (context, snapshot) {
                  // 1. Durum: Veri bekleniyor (Yükleniyor)
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator(color: Colors.cyanAccent));
                  }
                  // 2. Durum: Hata çıktı
                  else if (snapshot.hasError) {
                    return Center(child: Text('Hata: ${snapshot.error}', style: const TextStyle(color: Colors.red)));
                  }
                  // 3. Durum: Veri geldi ama liste boş
                  else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                    return const Center(child: Text('Henüz kayıtlı cihaz yok.', style: TextStyle(color: Colors.grey)));
                  }

                  // 4. Durum: Veriler hazır! Listele
                  final assetList = snapshot.data!;
                  return ListView.builder(
                    itemCount: assetList.length,
                    itemBuilder: (context, index) {
                      final asset = assetList[index];
                      return Card(
                        color: Colors.white10,
                        margin: const EdgeInsets.only(bottom: 10),
                        child: ListTile(
                          leading: Icon(
                            asset.durum ? Icons.check_circle : Icons.error,
                            color: asset.durum ? Colors.green : Colors.red,
                          ),
                          title: Text(asset.isim, style: const TextStyle(color: Colors.white)),
                          subtitle: Text("${asset.tur} - ${asset.seriNo}", style: const TextStyle(color: Colors.grey)),
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
      // EKLEME BUTONU
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          // Ekleme sayfasına git, dönüşte veriyi bekle
          final yeniVeriMap = await Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const AddAssetPage()),
          );

          if (yeniVeriMap != null) {
            // Gelen veriyi Model'e çevir
            Asset yeniAsset = Asset(
              isim: yeniVeriMap['isim'],
              tur: yeniVeriMap['tur'],
              seriNo: "SN-${DateTime.now().millisecondsSinceEpoch}", // Otomatik seri no (Test için)
              durum: true,
            );

            // API'ye Gönder
            try {
              bool basari = await _apiService.addAsset(yeniAsset);
              if (basari) {
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Kaydedildi!")));
                _refreshList(); // Listeyi güncelle
              } else {
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Kaydedilemedi!"), backgroundColor: Colors.red));
              }
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Hata: $e"), backgroundColor: Colors.red));
            }
          }
        },
        backgroundColor: Colors.cyanAccent,
        child: const Icon(Icons.add, color: Colors.black),
      ),
    );
  }

  // Yan Menü (Kod kalabalığı yapmasın diye buraya aldık)
  Widget _buildDrawer(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          const UserAccountsDrawerHeader(
            accountName: Text("Abdusamed"),
            accountEmail: Text("admin@yusiber.com"),
            currentAccountPicture: CircleAvatar(backgroundColor: Colors.cyanAccent, child: Icon(Icons.person, color: Colors.black)),
            decoration: BoxDecoration(color: Color(0xFF1E1E1E)),
          ),
          ListTile(
            leading: const Icon(Icons.exit_to_app, color: Colors.red),
            title: const Text('Çıkış'),
            onTap: () => Navigator.pop(context),
          ),
        ],
      ),
    );
  }
}