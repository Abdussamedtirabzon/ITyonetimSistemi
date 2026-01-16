using System;
using System.Collections.Generic;

namespace CyberAsset.API.Models;

public partial class PerformanceMetric
{
    public long Id { get; set; }

    public int AssetId { get; set; }

    public int? CpuUsagePercent { get; set; }

    public int? RamUsagePercent { get; set; }

    public int? DiskFreeSpaceGb { get; set; }

    public DateTime? RecordedAt { get; set; }

    public virtual Asset Asset { get; set; } = null!;
}
