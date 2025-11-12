using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class ChangeAdminCodeDeleteBehaviorToCascade : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_AdminCodes_Users_UsedByUserId",
                table: "AdminCodes");

            migrationBuilder.AddForeignKey(
                name: "FK_AdminCodes_Users_UsedByUserId",
                table: "AdminCodes",
                column: "UsedByUserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_AdminCodes_Users_UsedByUserId",
                table: "AdminCodes");

            migrationBuilder.AddForeignKey(
                name: "FK_AdminCodes_Users_UsedByUserId",
                table: "AdminCodes",
                column: "UsedByUserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.SetNull);
        }
    }
}
