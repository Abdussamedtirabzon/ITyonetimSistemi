using System;
using System.Collections.Generic;

namespace CyberAsset.API.Models;

public partial class User
{
    public int Id { get; set; }

    public int? DepartmentId { get; set; }

    public string Username { get; set; } = null!;

    public string FullName { get; set; } = null!;

    public string? Email { get; set; }

    public string PasswordHash { get; set; } = null!;

    public string? Role { get; set; }

    public bool? IsActive { get; set; }

    public DateTime? CreatedAt { get; set; }

    public virtual ICollection<Asset> Assets { get; set; } = new List<Asset>();

    public virtual Department? Department { get; set; }

    public virtual ICollection<Message> Messages { get; set; } = new List<Message>();
}
