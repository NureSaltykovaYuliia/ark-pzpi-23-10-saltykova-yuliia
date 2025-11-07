namespace Application.DTOs
{
    public class AdminCodeDto
    {
        public int Id { get; set; }
        public string Code { get; set; }
        public bool IsUsed { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? UsedAt { get; set; }
        public int? UsedByUserId { get; set; }
        public string? UsedByUsername { get; set; }
    }
}
