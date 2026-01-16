using System;
using System.Collections.Generic;

namespace CyberAsset.API.Models;

public partial class WebAccessLog
{
    public long Id { get; set; }

    public int AssetId { get; set; }

    public string? Url { get; set; }

    public string? Domain { get; set; }

    public bool? IsBlocked { get; set; }

    public DateTime? AccessTime { get; set; }

    public virtual Asset Asset { get; set; } = null!;
}
