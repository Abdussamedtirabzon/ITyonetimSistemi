class Asset {
  final int? id;
  final String isim;
  final String tur;
  final String seriNo;
  final bool durum; 

  Asset({
    this.id,
    required this.isim,
    required this.tur,
    required this.seriNo,
    required this.durum,
  });

  // API'den gelen veriyi Flutter'a çevir (GET işlemi için)
  factory Asset.fromJson(Map<String, dynamic> json) {
    return Asset(
      id: json['id'],
      isim: json['name'] ?? 'İsimsiz Cihaz', 
      // API'de 'assetTypeId' 1 ise Laptop diyelim, değilse Diğer.
      tur: (json['assetTypeId'] == 1) ? 'Laptop' : 'Diğer',
      // API'de seri no yok, o yüzden macAddress'i seri no gibi kullanıyoruz
      seriNo: json['macAddress'] ?? 'Yok',
      // API "Active" gönderiyor, biz bunu true'ya çeviriyoruz
      durum: json['status'] == 'Active',
    );
  }

  // Flutter verisini API'ye çevir (POST/Kayıt işlemi için)
  Map<String, dynamic> toJson() {
    return {
      'name': isim,
      // API bizden sayı istiyor. Şimdilik hepsine 1 (Laptop) diyelim.
      'assetTypeId': 1, 
      // Seri numarasını API'deki macAddress sütununa kaydedelim
      'macAddress': seriNo,
      'ipAddress': '192.168.1.100', // Boş gitmesin diye rastgele IP
      // Bizdeki true/false bilgisini API'nin diline ("Active") çevirelim
      'status': durum ? "Active" : "Passive",
    };
  }
}