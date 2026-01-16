import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/asset_model.dart';

class ApiService {
  // Senin port adresin 5219 idi, onu sabitliyoruz.
  static const String baseUrl = "http://localhost:5219/api"; 

  // 1. GET: Tüm Varlıkları Getir
  Future<List<Asset>> getAssets() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/assets'));
      if (response.statusCode == 200) {
        List<dynamic> body = jsonDecode(response.body);
        return body.map((item) => Asset.fromJson(item)).toList();
      } else {
        throw Exception('API Hatası: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Bağlantı Hatası: $e');
    }
  }

  // 2. POST: Yeni Varlık Ekle
  Future<bool> addAsset(Asset asset) async {
    final response = await http.post(
      Uri.parse('$baseUrl/assets'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(asset.toJson()),
    );
    return response.statusCode == 201 || response.statusCode == 200;
  }

  // 3. PUT: Varlık Güncelle (YENİ)
  Future<bool> updateAsset(Asset asset) async {
    // Güncelleme yaparken ID'yi adrese ekliyoruz (örn: .../assets/5)
    final response = await http.put(
      Uri.parse('$baseUrl/assets/${asset.id}'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(asset.toJson()),
    );
    return response.statusCode == 200 || response.statusCode == 204;
  }

  // 4. DELETE: Varlık Sil (YENİ)
  Future<bool> deleteAsset(int id) async {
    final response = await http.delete(Uri.parse('$baseUrl/assets/$id'));
    return response.statusCode == 200 || response.statusCode == 204;
  }
}