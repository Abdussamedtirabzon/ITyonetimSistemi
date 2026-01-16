using System;
using System.Collections.Generic;

namespace CyberAsset.API.Models;

public partial class UserAuditLog
{
    public long LogId { get; set; }

    public int? UserId { get; set; }

    public string? OldRole { get; set; }

    public string? NewRole { get; set; }

    public string? OperationType { get; set; }

    public DateTime? ChangedAt { get; set; }
}
