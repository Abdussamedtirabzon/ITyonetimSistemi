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
    final result = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => AddAssetPage(assetToEdit: assetToEdit)),
    );

    if (result != null) {
      Asset islemYapilacakAsset = Asset(
        id: result['id'],
        isim: result['isim'],
        tur: result['tur'],
        seriNo: result['seriNo'],
        durum: result['durum'],
      );

      bool basari;
      if (assetToEdit == null) {
        basari = await _apiService.addAsset(islemYapilacakAsset);
      } else {
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

  // SİLME İŞLEMİ
  Future<void> _silmeOnayi(Asset asset) async {
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
      // LAYOUT BUILDER: Ekran boyutuna göre karar veren bekçi
      body: LayoutBuilder(
        builder: (context, constraints) {
          // Eğer ekran genişliği 600'den büyükse MASAÜSTÜ görünümü
          if (constraints.maxWidth > 600) {
            return _buildDesktopTable();
          } else {
            // Değilse MOBİL görünümü
            return _buildMobileList();
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _navigateAndProcessAsset(),
        backgroundColor: Colors.cyanAccent,
        child: const Icon(Icons.add, color: Colors.black),
      ),
    );
  }

  // --- MOBİL GÖRÜNÜM (KARTLAR) ---
  Widget _buildMobileList() {
    return FutureBuilder<List<Asset>>(
      future: _assetsFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator(color: Colors.cyanAccent));
        if (!snapshot.hasData || snapshot.data!.isEmpty) return const Center(child: Text('Liste boş.'));

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: snapshot.data!.length,
          itemBuilder: (context, index) {
            final asset = snapshot.data![index];
            return Card(
              color: Colors.white10,
              margin: const EdgeInsets.only(bottom: 10),
              child: ListTile(
                onTap: () => _navigateAndProcessAsset(assetToEdit: asset),
                leading: Icon(
                  asset.durum ? Icons.check_circle : Icons.error,
                  color: asset.durum ? Colors.green : Colors.red,
                ),
                title: Text(asset.isim, style: const TextStyle(color: Colors.white)),
                subtitle: Text("${asset.tur} • ${asset.seriNo}", style: const TextStyle(color: Colors.grey)),
                trailing: IconButton(
                  icon: const Icon(Icons.delete, color: Colors.redAccent),
                  onPressed: () => _silmeOnayi(asset),
                ),
              ),
            );
          },
        );
      },
    );
  }

  // --- MASAÜSTÜ GÖRÜNÜM (TABLO) ---
  Widget _buildDesktopTable() {
    return FutureBuilder<List<Asset>>(
      future: _assetsFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator(color: Colors.cyanAccent));
        if (!snapshot.hasData || snapshot.data!.isEmpty) return const Center(child: Text('Liste boş.'));

        final assets = snapshot.data!;

        return SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Container(
            width: double.infinity, // Tabloyu tam genişliğe yay
            decoration: BoxDecoration(
              border: Border.all(color: Colors.white24),
              borderRadius: BorderRadius.circular(8),
            ),
            child: DataTable(
              headingRowColor: WidgetStateProperty.all(Colors.white10),
              dataRowColor: WidgetStateProperty.all(Colors.black12),
              columns: const [
                DataColumn(label: Text('Durum', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.cyanAccent))),
                DataColumn(label: Text('Cihaz Adı', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.cyanAccent))),
                DataColumn(label: Text('Tür', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.cyanAccent))),
                DataColumn(label: Text('Seri No / MAC', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.cyanAccent))),
                DataColumn(label: Text('İşlemler', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.cyanAccent))),
              ],
              rows: assets.map((asset) {
                return DataRow(cells: [
                  DataCell(Icon(
                    asset.durum ? Icons.check_circle : Icons.cancel,
                    color: asset.durum ? Colors.green : Colors.red,
                  )),
                  DataCell(Text(asset.isim, style: const TextStyle(color: Colors.white))),
                  DataCell(Text(asset.tur, style: const TextStyle(color: Colors.white70))),
                  DataCell(Text(asset.seriNo, style: const TextStyle(fontFamily: 'monospace', color: Colors.white70))),
                  DataCell(Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.edit, color: Colors.blueAccent),
                        onPressed: () => _navigateAndProcessAsset(assetToEdit: asset),
                        tooltip: "Düzenle",
                      ),
                      IconButton(
                        icon: const Icon(Icons.delete, color: Colors.redAccent),
                        onPressed: () => _silmeOnayi(asset),
                        tooltip: "Sil",
                      ),
                    ],
                  )),
                ]);
              }).toList(),
            ),
          ),
        );
      },
    );
  }
}