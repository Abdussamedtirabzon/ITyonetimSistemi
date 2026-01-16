using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using CyberAsset.API.Models;

namespace CyberAsset.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AssetsController : ControllerBase
    {
        private readonly CyberAssetDbContext _context;

        public AssetsController(CyberAssetDbContext context)
        {
            _context = context;
        }

        // 1. GET: Tüm Varlıkları Getir
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Asset>>> GetAssets()
        {
            return await _context.Assets.ToListAsync();
        }

       // 2. POST: Yeni Varlık Ekle
        [HttpPost]
        public async Task<ActionResult<Asset>> PostAsset(Asset asset)
        {
            // HATA BURADAYDI, DÜZELTTİK:
            // DateTime.Now yerine DateOnly.FromDateTime(DateTime.Now) kullandık.
            if (asset.PurchaseDate == null) 
            {
                asset.PurchaseDate = DateOnly.FromDateTime(DateTime.Now);
            }

            // LastSeen (Son Görülme) genelde saatli olur, o yüzden DateTime kalabilir.
            // Eğer bunda da hata verirse bunu da DateOnly yaparız.
            if (asset.LastSeen == null) 
            {
                asset.LastSeen = DateTime.Now; 
            }

            _context.Assets.Add(asset);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetAssets), new { id = asset.Id }, asset);
        }
        // 3. PUT: Varlık Güncelle (DÜZENLEME) - EKSİK OLAN BUYDU
       // 3. PUT: Varlık Güncelle (AKILLI GÜNCELLEME)
        [HttpPut("{id}")]
        public async Task<IActionResult> PutAsset(int id, Asset asset)
        {
            // 1. Önce veritabanındaki gerçek kaydı bulalım
            var existingAsset = await _context.Assets.FindAsync(id);
            
            // Eğer kayıt yoksa hata ver
            if (existingAsset == null)
            {
                return NotFound();
            }

            // 2. SADECE Flutter'dan gelen bilgileri değiştirelim.
            // Tarihlere, IP adresine vs. dokunmuyoruz, onlar aynen kalsın.
            existingAsset.Name = asset.Name;
            existingAsset.MacAddress = asset.MacAddress; // Seri No buraya gidiyor
            existingAsset.AssetTypeId = asset.AssetTypeId;
            existingAsset.Status = asset.Status; // Aktif/Pasif durumu

            // 3. Değişiklikleri Kaydet
            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                throw;
            }

            return NoContent(); // Başarılı (204)
        }

        // 4. DELETE: Varlık Sil (SİLME) - EKSİK OLAN BUYDU
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAsset(int id)
        {
            var asset = await _context.Assets.FindAsync(id);
            if (asset == null)
            {
                return NotFound();
            }

            _context.Assets.Remove(asset);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}