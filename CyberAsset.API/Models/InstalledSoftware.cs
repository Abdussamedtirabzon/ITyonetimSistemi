using System;
using System.Collections.Generic;

namespace CyberAsset.API.Models;

public partial class InstalledSoftware
{
    public int Id { get; set; }

    public int AssetId { get; set; }

    public string SoftwareName { get; set; } = null!;

    public string? Version { get; set; }

    public string? Publisher { get; set; }

    public DateTime? InstallDate { get; set; }

    public virtual Asset Asset { get; set; } = null!;
}
