using System;
using System.Collections.Generic;

namespace CyberAsset.API.Models;

public partial class Asset
{
    public int Id { get; set; }

    public int AssetTypeId { get; set; }

    public int? AssignedUserId { get; set; }

    public string Name { get; set; } = null!;

    public string? Ipaddress { get; set; }

    public string? MacAddress { get; set; }
    

    public string? OsName { get; set; }

    public string? OsVersion { get; set; }

    public string? SpecsCpu { get; set; }

    public int? SpecsRamGb { get; set; }

    public DateOnly? PurchaseDate { get; set; }

    public DateOnly? WarrantyEndDate { get; set; }

    public string? Status { get; set; }

    public DateTime? LastSeen { get; set; }

    public virtual AssetType? AssetType { get; set; } = null!;

    public virtual User? AssignedUser { get; set; }

    public virtual ICollection<DetectedVulnerability> DetectedVulnerabilities { get; set; } = new List<DetectedVulnerability>();

    public virtual ICollection<InstalledSoftware> InstalledSoftwares { get; set; } = new List<InstalledSoftware>();

    public virtual ICollection<PerformanceMetric> PerformanceMetrics { get; set; } = new List<PerformanceMetric>();

    public virtual ICollection<WebAccessLog> WebAccessLogs { get; set; } = new List<WebAccessLog>();
    // ... Eski alanlar (Id, Name, vs.) burada kalsın ...

    // YENİ EKLENECEK DETAY ALANLARI
    public string? CpuInfo { get; set; }    // Örn: Intel Core i7-12700H
    public string? RamCapacity { get; set; } // Örn: 16 GB
    public string? DiskCapacity { get; set; } // Örn: 512 GB SSD
}
