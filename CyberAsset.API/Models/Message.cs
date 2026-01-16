using System;
using System.Collections.Generic;

namespace CyberAsset.API.Models;

public partial class Message
{
    public long Id { get; set; }

    public int SenderUserId { get; set; }

    public int? ReceiverUserId { get; set; }

    public string? MessageText { get; set; }

    public string? AttachmentPath { get; set; }

    public DateTime? SentAt { get; set; }

    public bool? IsRead { get; set; }

    public virtual User SenderUser { get; set; } = null!;
}
