using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace CyberAsset.API.Migrations
{
    /// <inheritdoc />
    public partial class AjanSutunlari_Manual : Migration
    {
        /// <inheritdoc />
       protected override void Up(MigrationBuilder migrationBuilder)
        {
            // DİKKAT: Buradaki 'CreateTable' komutlarını SİLDİK.
            // Çünkü senin veritabanında tablolar zaten var.
            // Sadece eksik olan 4 YENİ SÜTUNU ekliyoruz:

            migrationBuilder.AddColumn<string>(
                name: "CpuInfo",
                table: "Assets",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "DiskCapacity",
                table: "Assets",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "OsVersion",
                table: "Assets",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "RamCapacity",
                table: "Assets",
                type: "nvarchar(max)",
                nullable: true);
        }
    }
}
