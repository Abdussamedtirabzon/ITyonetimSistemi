import 'package:flutter/material.dart';
import 'add_asset.dart';
import 'services/api_service.dart';
import 'models/asset_model.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final ApiService _apiService = ApiService();
  late Future<List<Asset>> _assetsFuture;

  @override
  void initState() {
    super.initState();
    _refreshList();
  }

  void _refreshList() {
    setState(() {
      _assetsFuture = _apiService.getAssets();
    });
  }

  // Ekleme veya Güncelleme İşlemini Yöneten Fonksiyon
  void _navigateAndProcessAsset({Asset? assetToEdit}) async {
    // Sayfaya git (Eğer assetToEdit doluysa düzenleme modu açılır)
    final result = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => AddAssetPage(assetToEdit: assetToEdit)),
    );

    if (result != null) {
      // Gelen veriyi Model'e çevir
      Asset islemYapilacakAsset = Asset(
        id: result['id'], // Düzenleme ise ID dolu gelir
        isim: result['isim'],
        tur: result['tur'],
        seriNo: result['seriNo'],
        durum: result['durum'],
      );

      bool basari;
      if (assetToEdit == null) {
        // ID yoksa EKLEME yap
        basari = await _apiService.addAsset(islemYapilacakAsset);
      } else {
        // ID varsa GÜNCELLEME yap
        basari = await _apiService.updateAsset(islemYapilacakAsset);
      }

      if (basari) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(assetToEdit == null ? "Eklendi!" : "Güncellendi!")),
        );
        _refreshList();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("İşlem Başarısız!"), backgroundColor: Colors.red));
      }
    }
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
          IconButton(icon: const Icon(Icons.refresh), onPressed: _refreshList),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: FutureBuilder<List<Asset>>(
          future: _assetsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator(color: Colors.cyanAccent));
            } else if (snapshot.hasError) {
              return Center(child: Text('Hata: ${snapshot.error}', style: const TextStyle(color: Colors.red)));
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return const Center(child: Text('Liste boş.', style: TextStyle(color: Colors.grey)));
            }

            final assetList = snapshot.data!;
            return ListView.builder(
              itemCount: assetList.length,
              itemBuilder: (context, index) {
                final asset = assetList[index];
                return Card(
                  color: Colors.white10,
                  margin: const EdgeInsets.only(bottom: 10),
                  child: ListTile(
                    // TIKLAYINCA DÜZENLEME MODU
                    onTap: () => _navigateAndProcessAsset(assetToEdit: asset),
                    
                    leading: Icon(
                      asset.durum ? Icons.check_circle : Icons.error,
                      color: asset.durum ? Colors.green : Colors.red,
                    ),
                    title: Text(asset.isim, style: const TextStyle(color: Colors.white)),
                    subtitle: Text("${asset.tur} • ${asset.seriNo}", style: const TextStyle(color: Colors.grey)),
                    
                    // SİLME BUTONU
                    trailing: IconButton(
                      icon: const Icon(Icons.delete, color: Colors.redAccent),
                      onPressed: () async {
                        bool? eminMi = await showDialog(
                          context: context,
                          builder: (c) => AlertDialog(
                            title: const Text("Siliniyor"),
                            content: Text("${asset.isim} silinsin mi?"),
                            actions: [
                              TextButton(onPressed: () => Navigator.pop(c, false), child: const Text("Hayır")),
                              TextButton(onPressed: () => Navigator.pop(c, true), child: const Text("Evet", style: TextStyle(color: Colors.red))),
                            ],
                          ),
                        );

                        if (eminMi == true && asset.id != null) {
                          await _apiService.deleteAsset(asset.id!);
                          _refreshList();
                        }
                      },
                    ),
                  ),
                );
              },
            );
          },
        ),
      ),
      // EKLEME BUTONU
      floatingActionButton: FloatingActionButton(
        onPressed: () => _navigateAndProcessAsset(), // Parametre vermezsek Ekleme Modu açılır
        backgroundColor: Colors.cyanAccent,
        child: const Icon(Icons.add, color: Colors.black),
      ),
    );
  }
}