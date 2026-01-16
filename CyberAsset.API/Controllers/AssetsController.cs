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
    }
}