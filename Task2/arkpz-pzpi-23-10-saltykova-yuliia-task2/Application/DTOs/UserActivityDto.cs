using System;

namespace Application.DTOs
{
    public class UserActivityDto
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Email { get; set; }
        public DateTime? LastActivity { get; set; }
        public bool IsBlocked { get; set; }
        public string? BlockReason { get; set; }
    }
}
