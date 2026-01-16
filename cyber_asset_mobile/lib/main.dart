import 'package:flutter/material.dart';
import 'dashboard.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false, // Sağ üstteki 'Debug' bandını kaldırır
      title: 'IT Yönetim Sistemi',
      theme: ThemeData(
        // Koyu tema (Cyber güvenlikçiye yakışır)
        brightness: Brightness.dark,
        primaryColor: const Color.fromARGB(255, 5, 133, 22),
        scaffoldBackgroundColor: const Color(0xFF1E1E1E),
        useMaterial3: true,
      ),
      home: const LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // 1. Logo veya Simge Alanı
              const Icon(
                Icons.security, // Güvenlik kalkanı ikonu
                size: 100,
                color: Colors.cyanAccent,
              ),
              const SizedBox(height: 20),
              
              // 2. Başlık
              const Text(
                'IT Yönetim Sistemi',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 10),
              const Text(
                'Hoş Geldiniz, lütfen giriş yapın.',
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 40),

              // 3. Kullanıcı Adı Kutusu
              TextField(
                decoration: InputDecoration(
                  labelText: 'Kullanıcı Adı',
                  prefixIcon: const Icon(Icons.person_outline),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  filled: true,
                  fillColor: Colors.white10,
                ),
              ),
              const SizedBox(height: 20),

              // 4. Şifre Kutusu
              TextField(
                obscureText: true, // Şifreyi gizle (****)
                decoration: InputDecoration(
                  labelText: 'Şifre',
                  prefixIcon: const Icon(Icons.lock_outline),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  filled: true,
                  fillColor: Colors.white10,
                ),
              ),
              const SizedBox(height: 30),

              // 5. Giriş Butonu
              SizedBox(
                width: double.infinity, // Butonu tam genişlik yap
                height: 50,
                child: ElevatedButton(
                  onPressed: () {
  // Sayfa Geçiş Kodu
  Navigator.pushReplacement(
    context,
    MaterialPageRoute(builder: (context) => const DashboardPage()),
  );
},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.cyanAccent,
                    foregroundColor: Colors.black, // Yazı rengi
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text(
                    'GİRİŞ YAP',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}