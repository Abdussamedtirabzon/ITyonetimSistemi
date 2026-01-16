import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/asset_model.dart';

class ApiService {
  // DİKKAT: Linux masaüstünde 'localhost' çalışır.
  // Waydroid veya Gerçek Telefonda bilgisayarın yerel IP'sini yazmalısın (Örn: 192.168.1.35)
  // ESKİSİ:
// static const String baseUrl = "http://localhost:5000/api";

// YENİSİ (Doğru Port):
static const String baseUrl = "http://localhost:5219/api";

  // Tüm Varlıkları Getir (GET)
  Future<List<Asset>> getAssets() async {
    final response = await http.get(Uri.parse('$baseUrl/assets'));

    if (response.statusCode == 200) {
      List<dynamic> body = jsonDecode(response.body);
      List<Asset> assets = body.map((dynamic item) => Asset.fromJson(item)).toList();
      return assets;
    } else {
      throw Exception('Varlıklar yüklenemedi: ${response.statusCode}');
    }
  }

  // Yeni Varlık Ekle (POST)
  Future<bool> addAsset(Asset asset) async {
    final response = await http.post(
      Uri.parse('$baseUrl/assets'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(asset.toJson()),
    );

    return response.statusCode == 201 || response.statusCode == 200;
  }
}