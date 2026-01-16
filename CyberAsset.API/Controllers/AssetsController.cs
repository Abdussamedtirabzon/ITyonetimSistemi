using Microsoft.AspNetCore.Mvc;
using CyberAsset.API.Models;
using Microsoft.EntityFrameworkCore;

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

        // GET: api/assets
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Asset>>> GetAssets()
        {
            return await _context.Assets.ToListAsync();
        }

        // POST: api/assets
        [HttpPost]
        public async Task<ActionResult<Asset>> PostAsset(Asset asset)
        {
            _context.Assets.Add(asset);
            await _context.SaveChangesAsync();
            return CreatedAtAction("GetAssets", new { id = asset.Id }, asset);
        }
    }
}