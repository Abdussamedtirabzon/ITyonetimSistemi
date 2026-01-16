using System;
using System.Collections.Generic;

namespace CyberAsset.API.Models;

public partial class AssetType
{
    public int Id { get; set; }

    public string TypeName { get; set; } = null!;

    public virtual ICollection<Asset> Assets { get; set; } = new List<Asset>();
}
