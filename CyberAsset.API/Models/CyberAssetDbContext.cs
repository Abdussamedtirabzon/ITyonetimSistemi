using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace CyberAsset.API.Models;

public partial class CyberAssetDbContext : DbContext
{
    public CyberAssetDbContext()
    {
    }

    public CyberAssetDbContext(DbContextOptions<CyberAssetDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Asset> Assets { get; set; }

    public virtual DbSet<AssetType> AssetTypes { get; set; }

    public virtual DbSet<Department> Departments { get; set; }

    public virtual DbSet<DetectedVulnerability> DetectedVulnerabilities { get; set; }

    public virtual DbSet<InstalledSoftware> InstalledSoftwares { get; set; }

    public virtual DbSet<Message> Messages { get; set; }

    public virtual DbSet<PerformanceMetric> PerformanceMetrics { get; set; }

    public virtual DbSet<User> Users { get; set; }

    public virtual DbSet<UserAuditLog> UserAuditLogs { get; set; }

    public virtual DbSet<VulnerabilityDefinition> VulnerabilityDefinitions { get; set; }

    public virtual DbSet<WebAccessLog> WebAccessLogs { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
        => optionsBuilder.UseSqlServer("Server=localhost,1433;Database=CyberAssetDB;User Id=sa;Password=Guclu.Sifre123!;TrustServerCertificate=True;");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Asset>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Assets__3214EC0783F18087");

            entity.HasIndex(e => e.Ipaddress, "IX_Assets_IPAddress");

            entity.HasIndex(e => e.Name, "IX_Assets_Name");

            entity.Property(e => e.Ipaddress)
                .HasMaxLength(50)
                .HasColumnName("IPAddress");
            entity.Property(e => e.LastSeen).HasColumnType("datetime");
            entity.Property(e => e.MacAddress).HasMaxLength(50);
            entity.Property(e => e.Name).HasMaxLength(100);
            entity.Property(e => e.OsName)
                .HasMaxLength(100)
                .HasColumnName("OS_Name");
            entity.Property(e => e.OsVersion)
                .HasMaxLength(50)
                .HasColumnName("OS_Version");
            entity.Property(e => e.SpecsCpu)
                .HasMaxLength(100)
                .HasColumnName("Specs_CPU");
            entity.Property(e => e.SpecsRamGb).HasColumnName("Specs_RAM_GB");
            entity.Property(e => e.Status)
                .HasMaxLength(20)
                .HasDefaultValue("Active");

            entity.HasOne(d => d.AssetType).WithMany(p => p.Assets)
                .HasForeignKey(d => d.AssetTypeId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK__Assets__AssetTyp__47DBAE45");

            entity.HasOne(d => d.AssignedUser).WithMany(p => p.Assets)
                .HasForeignKey(d => d.AssignedUserId)
                .OnDelete(DeleteBehavior.SetNull)
                .HasConstraintName("FK__Assets__Assigned__48CFD27E");
        });

        modelBuilder.Entity<AssetType>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__AssetTyp__3214EC07F2A25AEE");

            entity.Property(e => e.TypeName).HasMaxLength(50);
        });

        modelBuilder.Entity<Department>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Departme__3214EC07A145D2F1");

            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("(getdate())")
                .HasColumnType("datetime");
            entity.Property(e => e.ManagerName).HasMaxLength(100);
            entity.Property(e => e.Name).HasMaxLength(100);
        });

        modelBuilder.Entity<DetectedVulnerability>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Detected__3214EC07B4F9EB5A");

            entity.HasIndex(e => e.Status, "IX_DetectedVulns_Status");

            entity.Property(e => e.DetectedDate)
                .HasDefaultValueSql("(getdate())")
                .HasColumnType("datetime");
            entity.Property(e => e.FixedDate).HasColumnType("datetime");
            entity.Property(e => e.Status)
                .HasMaxLength(20)
                .HasDefaultValue("Open");

            entity.HasOne(d => d.Asset).WithMany(p => p.DetectedVulnerabilities)
                .HasForeignKey(d => d.AssetId)
                .HasConstraintName("FK__DetectedV__Asset__534D60F1");

            entity.HasOne(d => d.Vulnerability).WithMany(p => p.DetectedVulnerabilities)
                .HasForeignKey(d => d.VulnerabilityId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK__DetectedV__Vulne__5441852A");
        });

        modelBuilder.Entity<InstalledSoftware>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Installe__3214EC07DA6B4CF7");

            entity.ToTable("InstalledSoftware");

            entity.Property(e => e.InstallDate).HasColumnType("datetime");
            entity.Property(e => e.Publisher).HasMaxLength(100);
            entity.Property(e => e.SoftwareName).HasMaxLength(200);
            entity.Property(e => e.Version).HasMaxLength(50);

            entity.HasOne(d => d.Asset).WithMany(p => p.InstalledSoftwares)
                .HasForeignKey(d => d.AssetId)
                .HasConstraintName("FK__Installed__Asset__4BAC3F29");
        });

        modelBuilder.Entity<Message>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Messages__3214EC07CF991F32");

            entity.Property(e => e.AttachmentPath).HasMaxLength(500);
            entity.Property(e => e.IsRead).HasDefaultValue(false);
            entity.Property(e => e.SentAt)
                .HasDefaultValueSql("(getdate())")
                .HasColumnType("datetime");

            entity.HasOne(d => d.SenderUser).WithMany(p => p.Messages)
                .HasForeignKey(d => d.SenderUserId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK__Messages__Sender__6383C8BA");
        });

        modelBuilder.Entity<PerformanceMetric>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Performa__3214EC074A37688A");

            entity.Property(e => e.DiskFreeSpaceGb).HasColumnName("DiskFreeSpaceGB");
            entity.Property(e => e.RecordedAt)
                .HasDefaultValueSql("(getdate())")
                .HasColumnType("datetime");

            entity.HasOne(d => d.Asset).WithMany(p => p.PerformanceMetrics)
                .HasForeignKey(d => d.AssetId)
                .HasConstraintName("FK__Performan__Asset__59FA5E80");
        });

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Users__3214EC070687EF84");

            entity.ToTable(tb => tb.HasTrigger("trg_UserRoleAudit"));

            entity.HasIndex(e => e.Username, "UQ__Users__536C85E4CFED9F03").IsUnique();

            entity.HasIndex(e => e.Email, "UQ__Users__A9D105342CBF0A2F").IsUnique();

            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("(getdate())")
                .HasColumnType("datetime");
            entity.Property(e => e.Email).HasMaxLength(100);
            entity.Property(e => e.FullName).HasMaxLength(100);
            entity.Property(e => e.IsActive).HasDefaultValue(true);
            entity.Property(e => e.PasswordHash).HasMaxLength(500);
            entity.Property(e => e.Role)
                .HasMaxLength(20)
                .HasDefaultValue("User");
            entity.Property(e => e.Username).HasMaxLength(50);

            entity.HasOne(d => d.Department).WithMany(p => p.Users)
                .HasForeignKey(d => d.DepartmentId)
                .HasConstraintName("FK__Users__Departmen__3F466844");
        });

        modelBuilder.Entity<UserAuditLog>(entity =>
        {
            entity.HasKey(e => e.LogId).HasName("PK__UserAudi__5E5486487EF1719F");

            entity.Property(e => e.ChangedAt)
                .HasDefaultValueSql("(getdate())")
                .HasColumnType("datetime");
            entity.Property(e => e.NewRole).HasMaxLength(20);
            entity.Property(e => e.OldRole).HasMaxLength(20);
            entity.Property(e => e.OperationType).HasMaxLength(10);
        });

        modelBuilder.Entity<VulnerabilityDefinition>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Vulnerab__3214EC07D4856570");

            entity.HasIndex(e => e.CveCode, "UQ__Vulnerab__A5147B246776CBFC").IsUnique();

            entity.Property(e => e.CveCode)
                .HasMaxLength(50)
                .HasColumnName("CVE_Code");
            entity.Property(e => e.RiskLevel).HasMaxLength(20);
            entity.Property(e => e.SeverityScore).HasColumnType("decimal(3, 1)");
            entity.Property(e => e.Title).HasMaxLength(200);
        });

        modelBuilder.Entity<WebAccessLog>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__WebAcces__3214EC076D4A81C0");

            entity.Property(e => e.AccessTime)
                .HasDefaultValueSql("(getdate())")
                .HasColumnType("datetime");
            entity.Property(e => e.Domain).HasMaxLength(255);
            entity.Property(e => e.IsBlocked).HasDefaultValue(false);

            entity.HasOne(d => d.Asset).WithMany(p => p.WebAccessLogs)
                .HasForeignKey(d => d.AssetId)
                .HasConstraintName("FK__WebAccess__Asset__5EBF139D");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
