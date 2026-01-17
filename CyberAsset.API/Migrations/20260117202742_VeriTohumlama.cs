using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace CyberAsset.API.Migrations
{
    /// <inheritdoc />
    public partial class VeriTohumlama : Migration
    {
        /// <inheritdoc />
       protected override void Up(MigrationBuilder migrationBuilder)
        {
            // SQL Komutu: Eğer ID 1 veya 2 yoksa ekle, varsa pas geç.
            migrationBuilder.Sql(@"
                SET IDENTITY_INSERT AssetTypes ON;

                IF NOT EXISTS (SELECT * FROM AssetTypes WHERE Id = 1)
                BEGIN
                    INSERT INTO AssetTypes (Id, TypeName) VALUES (1, 'PC/Laptop');
                END

                IF NOT EXISTS (SELECT * FROM AssetTypes WHERE Id = 2)
                BEGIN
                    INSERT INTO AssetTypes (Id, TypeName) VALUES (2, 'Diğer');
                END

                SET IDENTITY_INSERT AssetTypes OFF;
            ");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "AssetTypes",
                keyColumn: "Id",
                keyValue: 1);

            migrationBuilder.DeleteData(
                table: "AssetTypes",
                keyColumn: "Id",
                keyValue: 2);
        }
    }
}
