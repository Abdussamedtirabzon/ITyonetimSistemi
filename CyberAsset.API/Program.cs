using CyberAsset.API.Models;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// 1. Controller'ları Sisteme Tanıt (Eksik olan buydu)
builder.Services.AddControllers();

// 2. Swagger (Test Ekranı) Ayarları
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// 3. Veritabanı Bağlantısı
// DİKKAT: Şifreni buraya doğru yazdığından emin ol!
builder.Services.AddDbContext<CyberAssetDbContext>(options =>
    options.UseSqlServer("Server=localhost,1433;Database=CyberAssetDB;User Id=sa;Password=Guclu.Sifre123!;TrustServerCertificate=True;"));

var app = builder.Build();

// 4. HTTP Ayarları
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();

// 5. Controller'ları Çalıştır
app.MapControllers();

app.Run();