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

        // 1. LİSTELEME
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Asset>>> GetAssets()
        {
            return await _context.Assets.ToListAsync();
        }

        // 2. TEKLİ GETİRME (DÜZENLEME İÇİN)
        [HttpGet("{id}")]
        public async Task<ActionResult<Asset>> GetAsset(int id)
        {
            var asset = await _context.Assets.FindAsync(id);
            if (asset == null) return NotFound();
            return asset;
        }

        // 3. EKLEME
        [HttpPost]
        public async Task<ActionResult<Asset>> PostAsset(Asset asset)
        {
            if (asset.PurchaseDate == default) asset.PurchaseDate = DateOnly.FromDateTime(DateTime.Now);
            if (asset.LastSeen == default) asset.LastSeen = DateTime.Now; 

            _context.Assets.Add(asset);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetAsset), new { id = asset.Id }, asset);
        }

        // 4. GÜNCELLEME (HATALI SATIRLAR SİLİNDİ)
        [HttpPut("{id}")]
        public async Task<IActionResult> PutAsset(int id, Asset asset)
        {
            var existingAsset = await _context.Assets.FindAsync(id);
            if (existingAsset == null) return NotFound();

            // Sadece var olan alanları güncelle
            existingAsset.Name = asset.Name;
            existingAsset.MacAddress = asset.MacAddress;
            existingAsset.AssetTypeId = asset.AssetTypeId;
            existingAsset.Status = asset.Status;
            
            // NOT: IpAddress satırlarını sildik çünkü Model'de henüz yok.
            // Kod artık hata vermeyecek.

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                throw;
            }

            return NoContent(); 
        }

        // 5. SİLME
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAsset(int id)
        {
            var asset = await _context.Assets.FindAsync(id);
            if (asset == null) return NotFound();

            _context.Assets.Remove(asset);
            await _context.SaveChangesAsync();

            return NoContent();
        }
        // 6. AKILLI KAYIT (UPSERT) - Hem Ajan Hem Nmap İçin
        // Cihaz MAC adresine göre aranır. Varsa güncellenir, yoksa yeni eklenir.
        [HttpPost("register")]
        public async Task<ActionResult<Asset>> RegisterAsset(Asset asset)
        {
            // 1. MAC Adresi boşsa kabul etme (Kimliksiz cihaz olmaz)
            if (string.IsNullOrEmpty(asset.MacAddress))
            {
                return BadRequest("MAC Adresi zorunludur!");
            }

            // 2. Veritabanında bu MAC adresine sahip cihaz var mı?
            var existingAsset = await _context.Assets
                                      .FirstOrDefaultAsync(a => a.MacAddress == asset.MacAddress);

            if (existingAsset != null)
            {
                // --- DURUM A: CİHAZ ZATEN VAR -> GÜNCELLE ---
                
                existingAsset.LastSeen = DateTime.Now; // "Ben buradayım" dediği an
                existingAsset.Ipaddress = asset.Ipaddress; // IP değişmiş olabilir
                existingAsset.Name = asset.Name; // İsmi değişmiş olabilir
                existingAsset.Status = "Active"; // Geri döndüyse Aktiftir

                // Donanım bilgileri değiştiyse güncelle (RAM takviyesi yapılmış olabilir)
                existingAsset.OsVersion = asset.OsVersion;
                existingAsset.CpuInfo = asset.CpuInfo;
                existingAsset.RamCapacity = asset.RamCapacity;
                existingAsset.DiskCapacity = asset.DiskCapacity;

                await _context.SaveChangesAsync();
                return Ok(existingAsset); // Güncellenmiş veriyi dön (200 OK)
            }
            else
            {
                // --- DURUM B: CİHAZ YOK -> YENİ EKLE ---
                
                if (asset.PurchaseDate == default) asset.PurchaseDate = DateOnly.FromDateTime(DateTime.Now);
                if (asset.LastSeen == default) asset.LastSeen = DateTime.Now;
                
                _context.Assets.Add(asset);
                await _context.SaveChangesAsync();

                return CreatedAtAction(nameof(GetAsset), new { id = asset.Id }, asset); // Yeni veri dön (201 Created)
            }
        }
    }
}